import logging

from fastapi import (
    HTTPException,
    BackgroundTasks,
    status,
    Request,
)

from api.api_v1.movies.crud import storage
from schemas.movie_description import MovieDescription


log = logging.getLogger(__name__)

UNSAFE_METHODS = frozenset(
    {
        "POST",
        "PUT",
        "PATCH",
        "DELETE",
    }
)


def prefetch_movie(movie_slug: str) -> MovieDescription:
    movie: MovieDescription | None = storage.get_movies_by_slug(slug=movie_slug)

    if movie:
        return movie

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Movie {movie_slug} not found",
    )


def save_storage_state(
    background_tasks: BackgroundTasks,
    request: Request,
):
    log.info("Методом запроса является %r", request.method)
    yield
    if request.method in UNSAFE_METHODS:
        log.info("Добавил background tasks в save storage")
        background_tasks.add_task(storage.save_state)
