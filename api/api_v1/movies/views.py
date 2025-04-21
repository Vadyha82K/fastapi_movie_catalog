from typing import Annotated

from fastapi import FastAPI, Depends
from api.api_v1.movies.crud import MOVIES_DESCRIPTION
from api.api_v1.movies.dependencies import prefetch_movie
from schemas.movie_description import MovieDescription

app = FastAPI(title="Movie Catalog")


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
