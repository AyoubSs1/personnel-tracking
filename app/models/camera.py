from dataclasses import dataclass
from typing import Optional


@dataclass
class Camera:
    id: Optional[int]
    camera_name: str
    location: str
    source: str
    source_type: str