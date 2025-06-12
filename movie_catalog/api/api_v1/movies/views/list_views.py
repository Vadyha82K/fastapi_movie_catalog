from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status,
)

from api.api_v1.movies.crud import MovieAlreadyExistsError, storage
from api.api_v1.movies.dependencies import (
    user_basic_auth_or_api_token_required_for_unsafe_methods,
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
        Depends(user_basic_auth_or_api_token_required_for_unsafe_methods),
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
    responses={
        status.HTTP_409_CONFLICT: {
            "description": "Фильм с таким слагом уже существует.",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "Фильм с slug='name' уже существует.",
                    },
                },
            },
        },
    },
)
def create_movie(
    movie_description_create: MovieDescriptionCreate,
) -> MovieDescription:
    try:
        return storage.create_or_raise_if_exists(movie_description_create)
    except MovieAlreadyExistsError as err:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Фильм с slug='{movie_description_create.slug}' уже существует.",
        ) from err
