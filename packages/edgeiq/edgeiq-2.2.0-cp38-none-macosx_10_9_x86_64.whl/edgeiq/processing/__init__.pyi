from .image_classification import ClassificationProcessor as ClassificationProcessor
from .instance_segmentation import InstanceSegmentationProcessor as InstanceSegmentationProcessor
from .libhuman_pose import PoseEstimationProcessor as PoseEstimationProcessor
from .object_detection import ObjectDetectionProcessor as ObjectDetectionProcessor
from .processor import Processor as Processor, ProcessorT as ProcessorT
from .semantic_segmentation import SemanticSegmentationProcessor as SemanticSegmentationProcessor

# Names in __all__ with no definition:
#   ReIdentificationProcessorload_trt_plugin
