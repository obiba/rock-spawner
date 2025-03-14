from typing import List, Optional
from pydantic import BaseModel

class PodRef(BaseModel):
    name: str
    image: str
    status: Optional[str] = "Pending"
    ip: Optional[str] = None
    port: Optional[int] = None

class PodRefs(BaseModel):
    items: List[PodRef] = []