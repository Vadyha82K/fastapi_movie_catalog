from fastapi import (
    APIRouter,
    status,
    BackgroundTasks,
)

from api.api_v1.movies.crud import storage
from schemas.movie_description import (
    MovieDescription,
    MovieDescriptionCreate,
    MovieDescriptionRead,
)

router = APIRouter(
    prefix="/movies",
    tags=["movies"],
)


@router.get(
    "/",
    response_model=list[MovieDescriptionRead],
)
def get_list_movies() -> list[MovieDescription]:
    return storage.get_list_movies()


@router.post(
    "/",
    response_model=MovieDescriptionRead,
    status_code=status.HTTP_201_CREATED,
)
def create_movie(
    movie_description_create: MovieDescriptionCreate,
    background_tasks: BackgroundTasks,
) -> MovieDescription:
    background_tasks.add_task(storage.save_state)
    return storage.create_movies(movie_description_create)
