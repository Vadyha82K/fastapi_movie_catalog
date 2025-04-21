from typing import Annotated

from fastapi import (
    FastAPI,
    Request,
    Depends,
)

from api.api_v1.movies.crud import MOVIES_DESCRIPTION
from api.api_v1.movies.dependencies import prefetch_movie
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


@app.get(
    "/movies/{movie_id}",
    response_model=MovieDescription,
)
def get_movie_description(
    movie: Annotated[MovieDescription, Depends(prefetch_movie)],
) -> MovieDescription:
    return movie
