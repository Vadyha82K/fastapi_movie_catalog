__all__ = ("storage",)

import logging
from typing import cast

from pydantic import BaseModel
from redis import Redis

from core import config
from schemas.movie_description import (
    MovieDescription,
    MovieDescriptionCreate,
    MovieDescriptionPartialUpdate,
    MovieDescriptionUpdate,
)

log = logging.getLogger(__name__)

redis = Redis(
    host=config.REDIS_HOST,
    port=config.REDIS_PORT,
    db=config.REDIS_DB_MOVIES,
    decode_responses=True,
)


class MovieBaseError(Exception):
    """
    Базовое исключение для действий с фильмами в CRUD.
    """


class MovieAlreadyExistsError(MovieBaseError):
    """
    Вызывается при создании фильма, если такой фильм уже существует.
    """


class MoviesStorage(BaseModel):

    @staticmethod
    def get_list_movies() -> list[MovieDescription]:
        return [
            MovieDescription.model_validate_json(value)
            for value in redis.hvals(name=config.REDIS_MOVIES_HASH_NAME)
        ]

    @staticmethod
    def get_movies_by_slug(slug: str) -> MovieDescription | None:
        result = redis.hget(
            name=config.REDIS_MOVIES_HASH_NAME,
            key=slug,
        )
        if result:
            return MovieDescription.model_validate_json(result)

        return None

    @staticmethod
    def exists(slug: str) -> bool:
        return cast(
            bool,
            redis.hexists(
                config.REDIS_MOVIES_HASH_NAME,
                key=slug,
            ),
        )

    def create_or_raise_if_exists(
        self,
        movie_description_create: MovieDescriptionCreate,
    ) -> MovieDescription:
        if not self.exists(movie_description_create.slug):
            return self.create_movies(movie_description_create)
        raise MovieAlreadyExistsError(movie_description_create.slug)

    @staticmethod
    def save_movies(movie: MovieDescription) -> MovieDescription:
        redis.hset(
            name=config.REDIS_MOVIES_HASH_NAME,
            key=movie.slug,
            value=movie.model_dump_json(),
        )
        return movie

    def create_movies(self, movie_in: MovieDescriptionCreate) -> MovieDescription:
        movie = MovieDescription(
            **movie_in.model_dump(),
        )
        self.save_movies(movie)
        log.info("Создана новая запись с фильмом %s", movie)
        return movie

    def update(
        self,
        movie: MovieDescription,
        movie_in: MovieDescriptionUpdate,
    ) -> MovieDescription:
        for field_name, value in movie_in:
            setattr(movie, field_name, value)
        self.save_movies(movie)
        log.info("Изменена запись с фильмом %s", movie)
        return movie

    def update_partial(
        self,
        movie: MovieDescription,
        movie_in: MovieDescriptionPartialUpdate,
    ) -> MovieDescription:
        for field_name, value in movie_in.model_dump(exclude_unset=True).items():
            setattr(movie, field_name, value)
        self.save_movies(movie)
        log.info("Частично изменена запись с фильмом %s", movie)
        return movie

    def delete_movies(self, slug: str) -> None:
        if self.get_movies_by_slug(slug):
            redis.hdel(
                config.REDIS_MOVIES_HASH_NAME,
                slug,
            )
            log.info("Удалена запись с фильмом %s", slug)

    def delete(self, movie: MovieDescription) -> None:
        self.delete_movies(slug=movie.slug)


storage = MoviesStorage()
