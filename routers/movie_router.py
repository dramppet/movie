from fastapi import APIRouter, HTTPException, Query
from typing import Optional, List

from models.movie_models import MovieCreate, MovieUpdate, MovieResponse
from services.movie_services import (
    create_movie,
    get_all_movies,
    get_movie_by_id,
    update_movie,
    delete_movie
)

router = APIRouter(prefix="/movies", tags=["Movies"])


@router.post("/", response_model=MovieResponse)
def create_movie_router(movie: MovieCreate):

    created_movie = create_movie(
        movie.title,
        movie.director,
        movie.release_year
    )

    return created_movie


@router.get("/", response_model=List[MovieResponse])
def get_movies_router(
    title: Optional[str] = Query(None),
    sort_by_rating: bool = Query(False)
):

    movies = get_all_movies(title, sort_by_rating)

    return movies


@router.get("/{movie_id}", response_model=MovieResponse)
def get_movie_router(movie_id: int):

    movie = get_movie_by_id(movie_id)

    if not movie:
        raise HTTPException(
            status_code=404,
            detail="Movie not found"
        )

    return movie


@router.put("/{movie_id}", response_model=MovieResponse)
def update_movie_router(movie_id: int, movie: MovieUpdate):

    updated = update_movie(
        movie_id,
        movie.title,
        movie.director,
        movie.release_year
    )

    if not updated:
        raise HTTPException(
            status_code=404,
            detail="Movie not found"
        )

    return get_movie_by_id(movie_id)


@router.delete("/{movie_id}")
def delete_movie_router(movie_id: int):

    deleted = delete_movie(movie_id)

    if not deleted:
        raise HTTPException(
            status_code=404,
            detail="Movie not found"
        )

    return {"message": "Movie deleted successfully"}