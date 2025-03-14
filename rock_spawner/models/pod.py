from typing import List, Optional
from pydantic import BaseModel

class PodRef(BaseModel):
    name: str
    image: str
    status: Optional[str] = "Pending"

class PodRefs(BaseModel):
    items: List[PodRef] = []