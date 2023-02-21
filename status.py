from pydantic import BaseModel
from enum import Enum


class ScriptStatus(str, Enum):
    work = "work"


class CameraStatus(str, Enum):
    online = "online"
    offline = "offline"


class Status(BaseModel):
    name: str
    script_status: ScriptStatus
    camera_status: CameraStatus
