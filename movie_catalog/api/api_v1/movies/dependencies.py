from fastapi import HTTPException
from starlette import status

from api.api_v1.movies.crud import MOVIES_DESCRIPTION
from schemas.movie_description import MovieDescription


def prefetch_movie(movie_id: int) -> MovieDescription:
    movie: MovieDescription | None = next(
        (movie for movie in MOVIES_DESCRIPTION if movie.id == movie_id),
        None,
    )
    if movie:
        return movie

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Movie {movie_id} not found",
    )
