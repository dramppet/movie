from pydantic import BaseModel, Field
from typing import Optional

class MovieBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=255)
    director: Optional[str] = Field(None, max_length=255)
    release_year: int = Field(..., ge=1888, le=2026)

class MovieCreate(MovieBase):
    pass

class MovieUpdate(MovieBase):
    ...

class MovieResponse(MovieBase):
    rating: Optional[float] = None

    @classmethod
    def from_query_result(cls, title, director, release_year, rating):
        return cls(
            title = title,
            director = director,
            release_year = release_year,
            rating = rating
        )