# -*- coding: utf-8 -*-
# File: dd.py

# Copyright 2021 Dr. Janis Meyer. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
Module for **deep**doctection analyzer.

-factory build_analyzer for a given config

-user factory with a reduced config setting
"""

import os
from os import environ
from shutil import copyfile
from typing import List, Optional, Tuple, Union

from ..extern.base import ObjectDetector
from ..extern.doctrocr import DoctrTextlineDetector, DoctrTextRecognizer
from ..extern.model import ModelCatalog, ModelDownloadManager
from ..extern.pdftext import PdfPlumberTextDetector
from ..extern.tessocr import TesseractOcrDetector
from ..extern.texocr import TextractOcrDetector
from ..pipe.base import PipelineComponent
from ..pipe.cell import DetectResultGenerator, SubImageLayoutService
from ..pipe.common import AnnotationNmsService, MatchingService, PageParsingService
from ..pipe.doctectionpipe import DoctectionPipe
from ..pipe.layout import ImageLayoutService
from ..pipe.order import TextOrderService
from ..pipe.refine import TableSegmentationRefinementService
from ..pipe.segment import PubtablesSegmentationService, TableSegmentationService
from ..pipe.text import TextExtractionService
from ..utils.file_utils import (
    boto3_available,
    detectron2_available,
    pytorch_available,
    tensorpack_available,
    tf_available,
)
from ..utils.fs import mkdir_p
from ..utils.logger import logger
from ..utils.metacfg import AttrDict, set_config_by_yaml
from ..utils.settings import LayoutType
from ..utils.systools import get_configs_dir_path, get_package_path
from ..utils.transform import PadTransform

if tf_available() and tensorpack_available():
    from tensorpack.utils.gpu import get_num_gpu  # pylint: disable=E0401

    from ..extern.tp.tfutils import disable_tp_layer_logging
    from ..extern.tpdetect import TPFrcnnDetector

if pytorch_available():
    from torch import cuda

    from ..extern.d2detect import D2FrcnnDetector, D2FrcnnTracingDetector
    from ..extern.hfdetr import HFDetrDerivedDetector

if boto3_available():
    from botocore.config import Config  # type: ignore


__all__ = ["get_dd_analyzer", "build_analyzer"]

_DD_ONE = "deepdoctection/configs/conf_dd_one.yaml"
_TESSERACT = "deepdoctection/configs/conf_tesseract.yaml"


def _auto_select_lib_and_device() -> Tuple[str, str]:
    """
    Select the DL library and subsequently the device. In summary:

    If TF is available, use TF unless a GPU is not available, in which case choose PT. If CUDA is not available and PT
    is not installed raise ImportError.
    """
    if tf_available() and tensorpack_available():
        if get_num_gpu() >= 1:
            return "TF", "cuda"
        if pytorch_available():
            return "PT", "cpu"
        raise ModuleNotFoundError("Install Pytorch and Torchvision to run with a CPU")
    if pytorch_available():
        if cuda.is_available():
            return "PT", "cuda"
        return "PT", "cpu"
    raise ModuleNotFoundError("Install Tensorflow or Pytorch before building analyzer")


def _maybe_copy_config_to_cache(file_name: str, force_copy: bool = True) -> str:
    """
    Initial copying of config file from the package dir into the config cache.

    :return: path to the copied file_name
    """

    absolute_path_source = os.path.join(get_package_path(), file_name)
    absolute_path = os.path.join(get_configs_dir_path(), os.path.join("dd", os.path.split(file_name)[1]))
    mkdir_p(os.path.split(absolute_path)[0])
    if not os.path.isfile(absolute_path) or force_copy:
        copyfile(absolute_path_source, absolute_path)
    return absolute_path


def _config_sanity_checks(cfg: AttrDict) -> None:
    if cfg.USE_PDF_MINER and cfg.USE_OCR and cfg.OCR.USE_DOCTR:
        raise ValueError("Configuration USE_PDF_MINER= True and USE_OCR=True and USE_DOCTR=True is not allowed")
    if cfg.OCR.USE_TESSERACT and (cfg.OCR.USE_DOCTR or cfg.OCR.USE_TEXTRACT):
        raise ValueError(
            "Configuration OCR.USE_TESSERACT=True and OCR.USE_DOCTR=True or OCR.USE_TEXTRACT=True is not "
            "allowed. Only one OCR system can be activated."
        )


def _build_detector(
    cfg: AttrDict, mode: str
) -> Union["D2FrcnnDetector", "TPFrcnnDetector", "HFDetrDerivedDetector", "D2FrcnnTracingDetector"]:
    weights = (
        getattr(cfg.TF, mode).WEIGHTS
        if cfg.LIB == "TF"
        else (getattr(cfg.PT, mode).WEIGHTS if detectron2_available() else getattr(cfg.PT, mode).WEIGHTS_TS)
    )
    filter_categories = (
        getattr(getattr(cfg.TF, mode), "FILTER") if cfg.LIB == "TF" else getattr(getattr(cfg.PT, mode), "FILTER")
    )
    config_path = ModelCatalog.get_full_path_configs(weights)
    weights_path = ModelDownloadManager.maybe_download_weights_and_configs(weights)
    profile = ModelCatalog.get_profile(weights)
    categories = profile.categories
    assert categories is not None
    if profile.model_wrapper in ("TPFrcnnDetector",):
        return TPFrcnnDetector(config_path, weights_path, categories, filter_categories=filter_categories)
    if profile.model_wrapper in ("D2FrcnnDetector",):
        return D2FrcnnDetector(
            config_path, weights_path, categories, device=cfg.DEVICE, filter_categories=filter_categories
        )
    if profile.model_wrapper in ("D2FrcnnTracingDetector",):
        return D2FrcnnTracingDetector(config_path, weights_path, categories, filter_categories=filter_categories)
    if profile.model_wrapper in ("HFDetrDerivedDetector",):
        preprocessor_config = ModelCatalog.get_full_path_preprocessor_configs(weights)
        return HFDetrDerivedDetector(
            config_path,
            weights_path,
            preprocessor_config,
            categories,
            device=cfg.DEVICE,
            filter_categories=filter_categories,
        )
    raise TypeError(
        f"You have chosen profile.model_wrapper: {profile.model_wrapper} which is not allowed. Please check "
        f"compatability with your deep learning framework"
    )


def _build_padder(cfg: AttrDict, mode: str) -> PadTransform:
    top, right, bottom, left = (
        getattr(cfg.PT, mode).PAD.TOP,
        getattr(cfg.PT, mode).PAD.RIGHT,
        getattr(cfg.PT, mode).PAD.BOTTOM,
        getattr(cfg.PT, mode).PAD.LEFT,
    )
    return PadTransform(top=top, right=right, bottom=bottom, left=left)


def _build_service(detector: ObjectDetector, cfg: AttrDict, mode: str) -> ImageLayoutService:
    padder = None
    if detector.__class__.__name__ in ("HFDetrDerivedDetector",):
        padder = _build_padder(cfg, mode)
    return ImageLayoutService(detector, to_image=True, crop_image=True, padder=padder)


def _build_sub_image_service(detector: ObjectDetector, cfg: AttrDict, mode: str) -> SubImageLayoutService:
    exclude_category_ids = []
    padder = None
    if mode == "ITEM":
        if detector.__class__.__name__ in ("HFDetrDerivedDetector",):
            exclude_category_ids.extend(["1", "3", "4", "5", "6"])
            padder = _build_padder(cfg, mode)
    detect_result_generator = DetectResultGenerator(detector.categories, exclude_category_ids=exclude_category_ids)
    return SubImageLayoutService(
        detector, [LayoutType.table, LayoutType.table_rotated], None, detect_result_generator, padder
    )


def _build_ocr(cfg: AttrDict) -> Union[TesseractOcrDetector, DoctrTextRecognizer, TextractOcrDetector]:
    if cfg.OCR.USE_TESSERACT:
        ocr_config_path = get_configs_dir_path() / cfg.OCR.CONFIG.TESSERACT
        return TesseractOcrDetector(
            ocr_config_path, config_overwrite=[f"LANGUAGES={cfg.LANGUAGE}"] if cfg.LANGUAGE is not None else None
        )
    if cfg.OCR.USE_DOCTR:
        weights = cfg.OCR.WEIGHTS.DOCTR_RECOGNITION.TF if cfg.LIB == "TF" else cfg.OCR.WEIGHTS.DOCTR_RECOGNITION.PT
        weights_path = ModelDownloadManager.maybe_download_weights_and_configs(weights)
        profile = ModelCatalog.get_profile(weights)
        if profile.architecture is None:
            raise ValueError("model profile.architecture must be specified")
        return DoctrTextRecognizer(profile.architecture, weights_path, cfg.DEVICE, lib=cfg.LIB)
    if cfg.OCR.USE_TEXTRACT:
        credentials_kwargs = {
            "aws_access_key_id": environ.get("ACCESS_KEY"),
            "aws_secret_access_key": environ.get("SECRET_KEY"),
            "config": Config(region_name=environ.get("REGION")),
        }
        return TextractOcrDetector(**credentials_kwargs)
    raise ValueError("You have set USE_OCR=True but any of USE_TESSERACT, USE_DOCTR, USE_TEXTRACT is set to False")


def _build_doctr_word(cfg: AttrDict) -> DoctrTextlineDetector:
    weights = cfg.OCR.WEIGHTS.DOCTR_WORD.TF if cfg.LIB == "TF" else cfg.OCR.WEIGHTS.DOCTR_WORD.PT
    weights_path = ModelDownloadManager.maybe_download_weights_and_configs(weights)
    profile = ModelCatalog.get_profile(weights)
    if profile.architecture is None:
        raise ValueError("model profile.architecture must be specified")
    if profile.categories is None:
        raise ValueError("model profile.categories must be specified")
    return DoctrTextlineDetector(profile.architecture, weights_path, profile.categories, cfg.DEVICE, lib=cfg.LIB)


def build_analyzer(cfg: AttrDict) -> DoctectionPipe:
    """
    Builds the analyzer with a given config

    :param cfg: A configuration
    :return: Analyzer pipeline
    """
    pipe_component_list: List[PipelineComponent] = []

    if cfg.USE_LAYOUT:
        d_layout = _build_detector(cfg, "LAYOUT")
        layout = _build_service(d_layout, cfg, "LAYOUT")
        pipe_component_list.append(layout)

    # setup layout nms service
    if cfg.LAYOUT_NMS_PAIRS.COMBINATIONS and cfg.USE_LAYOUT:
        if not isinstance(cfg.LAYOUT_NMS_PAIRS.COMBINATIONS, list) and not isinstance(
            cfg.LAYOUT_NMS_PAIRS.COMBINATIONS[0], list
        ):
            raise ValueError("LAYOUT_NMS_PAIRS mus be a list of lists")
        layout_nms_serivce = AnnotationNmsService(
            cfg.LAYOUT_NMS_PAIRS.COMBINATIONS, cfg.LAYOUT_NMS_PAIRS.THRESHOLDS, cfg.LAYOUT_NMS_PAIRS.PRIORITY
        )
        pipe_component_list.append(layout_nms_serivce)

    # setup tables service
    if cfg.USE_TABLE_SEGMENTATION:
        d_item = _build_detector(cfg, "ITEM")
        item = _build_sub_image_service(d_item, cfg, "ITEM")
        pipe_component_list.append(item)

        if d_item.__class__.__name__ not in ("HFDetrDerivedDetector",):
            d_cell = _build_detector(cfg, "CELL")
            cell = _build_sub_image_service(d_cell, cfg, "CELL")
            pipe_component_list.append(cell)

        if d_item.__class__.__name__ in ("HFDetrDerivedDetector",):
            pubtables = PubtablesSegmentationService(
                cfg.SEGMENTATION.ASSIGNMENT_RULE,
                cfg.SEGMENTATION.THRESHOLD_ROWS,
                cfg.SEGMENTATION.THRESHOLD_COLS,
                cfg.SEGMENTATION.FULL_TABLE_TILING,
                cfg.SEGMENTATION.REMOVE_IOU_THRESHOLD_ROWS,
                cfg.SEGMENTATION.REMOVE_IOU_THRESHOLD_COLS,
                cfg.SEGMENTATION.CELL_CATEGORY_ID,
                stretch_rule=cfg.SEGMENTATION.STRETCH_RULE,
            )
            pipe_component_list.append(pubtables)
        else:
            table_segmentation = TableSegmentationService(
                cfg.SEGMENTATION.ASSIGNMENT_RULE,
                cfg.SEGMENTATION.THRESHOLD_ROWS,
                cfg.SEGMENTATION.THRESHOLD_COLS,
                cfg.SEGMENTATION.FULL_TABLE_TILING,
                cfg.SEGMENTATION.REMOVE_IOU_THRESHOLD_ROWS,
                cfg.SEGMENTATION.REMOVE_IOU_THRESHOLD_COLS,
                cfg.SEGMENTATION.STRETCH_RULE,
            )
            pipe_component_list.append(table_segmentation)

            if cfg.USE_TABLE_REFINEMENT:
                table_segmentation_refinement = TableSegmentationRefinementService()
                pipe_component_list.append(table_segmentation_refinement)

    if cfg.USE_PDF_MINER:
        pdf_text = PdfPlumberTextDetector()
        d_text = TextExtractionService(pdf_text)
        pipe_component_list.append(d_text)

    # setup ocr
    if cfg.USE_OCR:
        # the extra mile for DocTr
        if cfg.OCR.USE_DOCTR:
            d_word = _build_doctr_word(cfg)
            word = ImageLayoutService(d_word, to_image=True, crop_image=True, skip_if_layout_extracted=True)
            pipe_component_list.append(word)

        ocr = _build_ocr(cfg)
        skip_if_text_extracted = cfg.USE_PDF_MINER
        extract_from_roi = LayoutType.word if cfg.OCR.USE_DOCTR else None
        text = TextExtractionService(
            ocr, skip_if_text_extracted=skip_if_text_extracted, extract_from_roi=extract_from_roi
        )
        pipe_component_list.append(text)

    if cfg.USE_PDF_MINER or cfg.USE_OCR:
        match = MatchingService(
            parent_categories=cfg.WORD_MATCHING.PARENTAL_CATEGORIES,
            child_categories=LayoutType.word,
            matching_rule=cfg.WORD_MATCHING.RULE,
            threshold=cfg.WORD_MATCHING.THRESHOLD,
            max_parent_only=cfg.WORD_MATCHING.MAX_PARENT_ONLY,
        )
        pipe_component_list.append(match)

        order = TextOrderService(
            text_container=LayoutType.word,
            text_block_categories=cfg.TEXT_ORDERING.TEXT_BLOCK_CATEGORIES,
            floating_text_block_categories=cfg.TEXT_ORDERING.FLOATING_TEXT_BLOCK_CATEGORIES,
            include_residual_text_container=cfg.TEXT_ORDERING.INCLUDE_RESIDUAL_TEXT_CONTAINER,
            starting_point_tolerance=cfg.TEXT_ORDERING.STARTING_POINT_TOLERANCE,
            broken_line_tolerance=cfg.TEXT_ORDERING.BROKEN_LINE_TOLERANCE,
            height_tolerance=cfg.TEXT_ORDERING.HEIGHT_TOLERANCE,
            paragraph_break=cfg.TEXT_ORDERING.PARAGRAPH_BREAK,
        )
        pipe_component_list.append(order)

    page_parsing_service = PageParsingService(
        text_container=LayoutType.word,
        floating_text_block_categories=cfg.TEXT_ORDERING.FLOATING_TEXT_BLOCK_CATEGORIES,
        include_residual_text_container=cfg.TEXT_ORDERING.INCLUDE_RESIDUAL_TEXT_CONTAINER,
    )
    pipe = DoctectionPipe(pipeline_component_list=pipe_component_list, page_parsing_service=page_parsing_service)

    return pipe


def get_dd_analyzer(reset_config_file: bool = False, config_overwrite: Optional[List[str]] = None) -> DoctectionPipe:
    """
    Factory function for creating the built-in **deep**doctection analyzer.

    The Standard Analyzer is a pipeline that comprises the following analysis components:

    - Document layout analysis

    - Table segmentation

    - Text extraction/OCR

    - Reading order

    We refer to the various notebooks and docs for running an analyzer and changing the configs.

    :param reset_config_file: This will copy the `.yaml` file with default variables to the `.cache` and therefore
                              resetting all configurations if set to `True`.
    :param config_overwrite: Passing a list of string arguments and values to overwrite the `.yaml` configuration with
                             highest priority, e.g. ["USE_TABLE_SEGMENTATION=False",
                                                     "USE_OCR=False",
                                                     "TF.LAYOUT.WEIGHTS=my_fancy_pytorch_model"]

    :return: A DoctectionPipe instance with given configs
    """
    config_overwrite = [] if config_overwrite is None else config_overwrite
    lib, device = _auto_select_lib_and_device()
    dd_one_config_path = _maybe_copy_config_to_cache(_DD_ONE, reset_config_file)
    _maybe_copy_config_to_cache(_TESSERACT)

    # Set up of the configuration and logging
    cfg = set_config_by_yaml(dd_one_config_path)

    cfg.freeze(freezed=False)
    cfg.LANGUAGE = None
    cfg.LIB = lib
    cfg.DEVICE = device
    cfg.freeze()

    if config_overwrite:
        cfg.update_args(config_overwrite)

    _config_sanity_checks(cfg)
    logger.info("Config: \n %s", str(cfg), cfg.to_dict())

    # will silent all TP logging while building the tower
    if tensorpack_available():
        disable_tp_layer_logging()

    return build_analyzer(cfg)
