import random
from typing import Annotated
from random import randint

from fastapi import (
    APIRouter,
    Depends,
    status,
    Form,
)

from api.api_v1.movies.crud import MOVIES_DESCRIPTION
from api.api_v1.movies.dependencies import prefetch_movie
from schemas.movie_description import MovieDescription


router = APIRouter(
    prefix="/movies",
    tags=["movies"],
)


@router.get(
    "/",
    response_model=list[MovieDescription],
)
def get_list_movies():
    return MOVIES_DESCRIPTION


@router.post(
    "/",
    response_model=MovieDescription,
    status_code=status.HTTP_201_CREATED,
)
def create_movie(
    title: Annotated[str, Form()],
    description: Annotated[str, Form()],
    genre: Annotated[list[str], Form()],
    release_year: Annotated[int, Form()],
):
    return MovieDescription(
        id=random.randint(1, 10000),
        title=title,
        description=description,
        genre=genre,
        release_year=release_year,
    )


@router.get(
    "/{movie_id}",
    response_model=MovieDescription,
)
def get_movie_description(
    movie: Annotated[MovieDescription, Depends(prefetch_movie)],
) -> MovieDescription:
    return movie
