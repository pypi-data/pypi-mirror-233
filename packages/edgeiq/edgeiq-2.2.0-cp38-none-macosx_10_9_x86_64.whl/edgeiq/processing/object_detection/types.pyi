import numpy as np
from typing import Any, List, Tuple

class ObjectDetectionPreProcessParams:
    image: np.ndarray
    size: Tuple[int, int]
    scalefactor: float
    mean: Tuple[float, float, float]
    swaprb: bool
    crop: bool
    def __init__(self, image, size, scalefactor, mean, swaprb, crop) -> None: ...

class ObjectDetectionPreProcessBatchParams:
    images: List[np.ndarray]
    size: Tuple[int, int]
    scalefactor: float
    mean: Tuple[float, float, float]
    swaprb: bool
    crop: bool
    def __init__(self, images, size, scalefactor, mean, swaprb, crop) -> None: ...

class ObjectDetectionPostProcessParams:
    results: Any
    image: np.ndarray
    confidence_level: float
    overlap_threshold: float
    num_classes: int
    model_input_size: Tuple[int, int]
    def __init__(self, results, image, confidence_level, overlap_threshold, num_classes, model_input_size) -> None: ...

class ObjectDetectionPostProcessBatchParams:
    results: List[Any]
    images: List[np.ndarray]
    confidence_level: float
    overlap_threshold: float
    num_classes: int
    model_input_size: Tuple[int, int]
    def __init__(self, results, images, confidence_level, overlap_threshold, num_classes, model_input_size) -> None: ...
