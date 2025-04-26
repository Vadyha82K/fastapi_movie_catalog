from fastapi import HTTPException
from starlette import status

from api.api_v1.movies.crud import storage
from schemas.movie_description import MovieDescription


def prefetch_movie(movie_slug: str) -> MovieDescription:
    movie: MovieDescription | None = storage.get_movies_by_slug(slug=movie_slug)

    if movie:
        return movie

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Movie {movie_slug} not found",
    )
