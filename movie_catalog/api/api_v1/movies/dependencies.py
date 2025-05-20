import logging
from typing import Annotated

from fastapi import (
    HTTPException,
    BackgroundTasks,
    status,
    Request,
    Depends,
)
from fastapi.security import (
    HTTPBearer,
    HTTPAuthorizationCredentials,
    HTTPBasic,
    HTTPBasicCredentials,
)
from starlette.status import HTTP_401_UNAUTHORIZED

from api.api_v1.movies.crud import storage
from api.api_v1.auth.services import (
    redis_tokens,
    redis_users,
)
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


static_api_token = HTTPBearer(
    scheme_name="Static API token",
    description="Your **Static API token** from developer portal. [Read more](#)",
    auto_error=False,
)

user_basic_auth = HTTPBasic(
    scheme_name="Basic auth",
    description="Basic username and password",
    auto_error=False,
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


def validate_basic_auth(
    credentials: HTTPBasicCredentials,
):
    if redis_users.validate_user_password(
        username=credentials.username,
        password=credentials.password,
    ):
        return

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="User credentials required. Invalid username or password.",
        headers={"WWW-Authenticate": "Basic"},
    )


def validate_api_token(
    api_token: HTTPAuthorizationCredentials,
):
    if redis_tokens.token_exists(
        api_token.credentials,
    ):
        return

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid API token",
    )


def user_basic_auth_or_api_token_required_for_unsafe_methods(
    request: Request,
    credentials: Annotated[
        HTTPBasicCredentials | None,
        Depends(user_basic_auth),
    ],
    api_token: Annotated[
        HTTPAuthorizationCredentials | None,
        Depends(static_api_token),
    ],
) -> None:

    if request.method not in UNSAFE_METHODS:
        return

    if credentials:
        return validate_basic_auth(credentials=credentials)

    if api_token:
        return validate_api_token(api_token=api_token)

    raise HTTPException(
        status_code=HTTP_401_UNAUTHORIZED,
        detail="Basic auth or API token required",
    )
