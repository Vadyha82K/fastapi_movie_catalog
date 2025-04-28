from fastapi import (
    APIRouter,
    status,
)

from api.api_v1.movies.crud import storage
from schemas.movie_description import (
    MovieDescription,
    MovieDescriptionCreate,
)

router = APIRouter(
    prefix="/movies",
    tags=["movies"],
)


@router.get(
    "/",
    response_model=list[MovieDescription],
)
def get_list_movies() -> list[MovieDescription]:
    return storage.get_list_movies()


@router.post(
    "/",
    response_model=MovieDescription,
    status_code=status.HTTP_201_CREATED,
)
def create_movie(
    movie_description_create: MovieDescriptionCreate,
) -> MovieDescription:
    return storage.create_movies(movie_description_create)
