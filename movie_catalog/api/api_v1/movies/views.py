from typing import Annotated

from fastapi import (
    APIRouter,
    Depends,
    status,
)

from api.api_v1.movies.crud import storage
from api.api_v1.movies.dependencies import prefetch_movie
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


@router.get(
    "/{movie_slug}",
    response_model=MovieDescription,
)
def get_movie_description(
    movie: Annotated[MovieDescription, Depends(prefetch_movie)],
) -> MovieDescription:
    return movie
