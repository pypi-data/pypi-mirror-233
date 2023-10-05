from _typeshed import Incomplete
from enum import Enum

APP_ROOT: Incomplete
MODELS_DIR: Incomplete
CREDENTIALS_DIR: Incomplete
HAILO_VID: str
HAILO_PID: str
CUDA_SUPPORTED_BOARDS: Incomplete
TEGRA_MODEL_PATH: str
HAILO_SUPPORTED_OS: Incomplete
QAIC_SUPPORTED_OS: Incomplete

class SupportedDevices(str, Enum):
    NANO: str
    XAVIER_NX: str
    AGX_XAVIER: str
    AGX_ORIN: str

DISABLE_VALIDATION: Incomplete
EDGEIQ_LOGS: Incomplete
