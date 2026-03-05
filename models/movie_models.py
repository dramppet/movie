from pydantic import BaseModel,Field
from typing import Optional
from datetime import datetime

class MovieBase(BaseModel):
    title: str = Field(..., min_length=1)
    director: Optional[str] = None
    release_year: Optional[int] = Field(None, ge=1888, le=2100)


class MovieCreate(MovieBase):
    pass


class MovieUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1)
    director: Optional[str] = None
    release_year: Optional[int] = Field(None, ge=1888, le=2100)


class MovieResponse(MovieBase):
    id: int
    rating: Optional[float]
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True