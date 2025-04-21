from typing import Annotated

from fastapi import (
    FastAPI,
    Request,
    Depends,
    HTTPException,
    status,
)

from api.api_v1.movies.crud import MOVIES_DESCRIPTION
from schemas.movie_description import MovieDescription

app = FastAPI(title="Movie Catalog")


@app.get("/")
def read_root(request: Request, name: str = "Guest"):
    docs_url = request.url.replace(
        path="/docs",
        query="",
    )

    return {
        "message": f"Hello {name}!",
        "docs": str(docs_url),
    }


@app.get(
    "/movies/",
    response_model=list[MovieDescription],
)
def get_list_movies():
    return MOVIES_DESCRIPTION


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


@app.get(
    "/movies/{movie_id}",
    response_model=MovieDescription,
)
def get_movie_description(
    movie: Annotated[MovieDescription, Depends(prefetch_movie)],
) -> MovieDescription:
    return movie
