from pydantic import BaseModel, validator
from typing import List, Optional


class SlideContent(BaseModel):

    headline: str
    bullets: List[str]
    visual: str = "bullets"
    metrics: Optional[List[str]] = None

    @validator("visual")
    def validate_visual(cls, v):

        allowed = ["bullets", "metrics", "chart", "image"]

        if v not in allowed:
            return "bullets"

        return v