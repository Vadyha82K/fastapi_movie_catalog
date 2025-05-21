import logging

from pydantic import BaseModel
from redis import Redis

from core import config
from schemas.movie_description import (
    MovieDescription,
    MovieDescriptionCreate,
    MovieDescriptionUpdate,
    MovieDescriptionPartialUpdate,
)

log = logging.getLogger(__name__)

redis = Redis(
    host=config.REDIS_HOST,
    port=config.REDIS_PORT,
    db=config.REDIS_DB_MOVIES,
    decode_responses=True,
)


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
            movie = MovieDescription.model_validate_json(result)
            return movie

    @staticmethod
    def save_movies(movie):
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
