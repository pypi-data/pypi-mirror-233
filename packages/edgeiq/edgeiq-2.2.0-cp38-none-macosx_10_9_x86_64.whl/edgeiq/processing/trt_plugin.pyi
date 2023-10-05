from edgeiq._constants import EDGEIQ_LOGS as EDGEIQ_LOGS
from edgeiq.tools import find_nvidia_gpu as find_nvidia_gpu, get_gpu_archs as get_gpu_archs, is_jetson as is_jetson, is_jetson_agx_orin as is_jetson_agx_orin, is_jetson_agx_xavier as is_jetson_agx_xavier, is_jetson_nano as is_jetson_nano, is_jetson_xavier_nx as is_jetson_xavier_nx
from typing import List

compute_architecture: List[str]

def load_trt_plugin() -> None: ...
