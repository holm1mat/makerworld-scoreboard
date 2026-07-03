from typing import Optional
from pydantic import BaseModel


class MakerWorldStats(BaseModel):
    capturedAt: str
    source: str
    handle: str
    collects: Optional[int]
    downloads: Optional[int]
    prints: Optional[int]
    boosts: Optional[int]
    followers: Optional[int]
    likes: Optional[int]