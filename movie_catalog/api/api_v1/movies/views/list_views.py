from fastapi import (
    APIRouter,
    status,
    Depends,
)

from api.api_v1.movies.crud import storage
from api.api_v1.movies.dependencies import (
    save_storage_state,
    user_basic_auth_required,
)
from schemas.movie_description import (
    MovieDescription,
    MovieDescriptionCreate,
    MovieDescriptionRead,
)

router = APIRouter(
    prefix="/movies",
    tags=["movies"],
    dependencies=[
        Depends(user_basic_auth_required),
        Depends(save_storage_state),
    ],
    responses={
        status.HTTP_401_UNAUTHORIZED: {
            "description": "Unauthenticated. Only for unsafe methods.",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "Invalid API Token",
                    },
                },
            },
        },
    },
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
