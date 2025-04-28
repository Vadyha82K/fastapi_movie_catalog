from typing import Annotated

from fastapi import Depends, APIRouter
from starlette import status

from api.api_v1.movies.crud import storage
from api.api_v1.movies.dependencies import prefetch_movie
from schemas.movie_description import MovieDescription


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
    response_model=MovieDescription,
)
def get_movie_description(
    movie: Annotated[MovieDescription, Depends(prefetch_movie)],
) -> MovieDescription:
    return movie


@router.delete(
    "/",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_movie(
    movie: Annotated[
        MovieDescription,
        Depends(prefetch_movie),
    ],
) -> None:
    storage.delete(movie=movie)
