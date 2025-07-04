from typing import Annotated

from fastapi import (
    APIRouter,
    Depends,
)
from starlette import status

from api.api_v1.movies.crud import storage
from api.api_v1.movies.dependencies import prefetch_movie
from schemas.movie_description import (
    MovieDescription,
    MovieDescriptionPartialUpdate,
    MovieDescriptionRead,
    MovieDescriptionUpdate,
)

MovieDescriptionBySlug = Annotated[
    MovieDescription,
    Depends(prefetch_movie),
]

router = APIRouter(
    prefix="/{slug}",
    responses={
        status.HTTP_404_NOT_FOUND: {
            "description": "Movies not found",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "Movies 'slug' not found",
                    },
                },
            },
        },
    },
)


@router.get(
    "/",
    response_model=MovieDescriptionRead,
)
def get_movie_description(
    movie: Annotated[MovieDescription, Depends(prefetch_movie)],
) -> MovieDescription:
    return movie


@router.put(
    "/",
    response_model=MovieDescriptionRead,
)
def update(
    movie: MovieDescriptionBySlug,
    movie_in: MovieDescriptionUpdate,
) -> MovieDescription:
    return storage.update(
        movie=movie,
        movie_in=movie_in,
    )


@router.patch(
    "/",
    response_model=MovieDescriptionRead,
)
def update_partial(
    movie: MovieDescriptionBySlug,
    movie_in: MovieDescriptionPartialUpdate,
) -> MovieDescription:
    return storage.update_partial(
        movie=movie,
        movie_in=movie_in,
    )


@router.delete(
    "/",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_movie(
    movie: MovieDescriptionBySlug,
) -> None:
    storage.delete(movie=movie)
