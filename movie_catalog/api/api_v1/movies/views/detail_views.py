from typing import Annotated

from fastapi import (
    Depends,
    APIRouter,
    BackgroundTasks,
)
from starlette import status

from api.api_v1.movies.crud import storage
from api.api_v1.movies.dependencies import prefetch_movie
from schemas.movie_description import (
    MovieDescription,
    MovieDescriptionUpdate,
    MovieDescriptionPartialUpdate,
    MovieDescriptionRead,
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
    background_tasks: BackgroundTasks,
):
    background_tasks.add_task(storage.save_state)
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
    background_tasks: BackgroundTasks,
) -> MovieDescription:
    background_tasks.add_task(storage.save_state)
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
    background_tasks: BackgroundTasks,
) -> None:
    background_tasks.add_task(storage.save_state)
    storage.delete(movie=movie)
