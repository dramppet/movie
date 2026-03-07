from fastapi import APIRouter, Depends, BackgroundTasks
from models.movie_models import MovieCreate, MovieUpdate, MovieResponse
from services import movie_services
from services.rating_service import enrich_movie_rating
from auth.security import  admin_required

router = APIRouter(prefix="/movies", tags=["Movies"])


@router.post("/")
def create_movie(
        movie: MovieCreate,
        background_tasks: BackgroundTasks,
        user=Depends(admin_required)):

    created_movie = movie_services.create_movie(movie)

    background_tasks.add_task(
        enrich_movie_rating,
        created_movie["id"],
        created_movie["title"]
    )

    return created_movie


@router.get("/")
def get_movies(
        title: str = None,
        raiting: str | None = None
):
    return movie_services.get_movies(title, raiting)


@router.get("/{movie_id}", response_model=MovieResponse)
def get_movie(
        movie_id: int):
    return movie_services.get_movie_id(movie_id)


@router.put("/{movie_id}")
def update_movie(
        movie_id: int,
        movie: MovieUpdate,
        user=Depends(admin_required)
):
    return movie_services.update_movie(movie_id,movie)


@router.delete("/{movie_id}")
def delete_movie(
        movie_id: int,
        user=Depends(admin_required)
):
    return movie_services.delete_movie(movie_id)