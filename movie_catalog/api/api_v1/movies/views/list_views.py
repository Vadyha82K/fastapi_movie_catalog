from fastapi import (
    APIRouter,
    status,
    Depends,
)

from api.api_v1.movies.crud import storage
from api.api_v1.movies.dependencies import save_storage_state
from schemas.movie_description import (
    MovieDescription,
    MovieDescriptionCreate,
    MovieDescriptionRead,
)

router = APIRouter(
    prefix="/movies",
    tags=["movies"],
    dependencies=[Depends(save_storage_state)],
)


@router.get(
    "/",
    response_model=list[MovieDescriptionRead],
)
def get_list_movies() -> list[MovieDescription]:
    return storage.get_list_movies()


@router.post(
    "/",
    response_model=MovieDescriptionRead,
    status_code=status.HTTP_201_CREATED,
)
def create_movie(
    movie_description_create: MovieDescriptionCreate,
) -> MovieDescription:
    return storage.create_movies(movie_description_create)
