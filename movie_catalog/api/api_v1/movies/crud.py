import logging

from pydantic import (
    BaseModel,
    ValidationError,
)
from fastapi import status, HTTPException

from core.config import MOVIES_STORAGE_FILEPATH
from schemas.movie_description import (
    MovieDescription,
    MovieDescriptionCreate,
    MovieDescriptionUpdate,
    MovieDescriptionPartialUpdate,
)

log = logging.getLogger(__name__)


class MoviesStorage(BaseModel):
    slug_to_movies: dict[str, MovieDescription] = {}

    def save_state(self) -> None:
        MOVIES_STORAGE_FILEPATH.write_text(self.model_dump_json(indent=2))
        log.info("Запись успешно сохранена.")

    @classmethod
    def from_state(cls) -> "MoviesStorage":
        if not MOVIES_STORAGE_FILEPATH.exists():
            return MoviesStorage()
        return cls.model_validate_json(MOVIES_STORAGE_FILEPATH.read_text())

    def init_storage_from_state(self) -> None:
        try:
            data = MoviesStorage.from_state()
            log.warning("Чтение данных с диска прошло успешно.")
        except ValidationError:
            self.save_state()
            log.warning("Файл был перезаписан, из-за невозможности прочитать данные.")
            return
        self.slug_to_movies.update(
            data.slug_to_movies,
        )

    def get_list_movies(self) -> list[MovieDescription]:
        return list(self.slug_to_movies.values())

    def get_movies_by_slug(self, slug: str) -> MovieDescription | None:
        result = self.slug_to_movies.get(slug)
        if result:
            return result
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Movie {slug} not found",
        )

    def create_movies(self, movie_in: MovieDescriptionCreate) -> MovieDescription:
        movie = MovieDescription(
            **movie_in.model_dump(),
        )
        self.slug_to_movies[movie.slug] = movie
        log.info("Создана новая запись с фильмом.")
        self.save_state()
        return movie

    def update(
        self,
        movie: MovieDescription,
        movie_in: MovieDescriptionUpdate,
    ) -> MovieDescription:
        for field_name, value in movie_in:
            setattr(movie, field_name, value)
        self.save_state()
        return movie

    def update_partial(
        self,
        movie: MovieDescription,
        movie_in: MovieDescriptionPartialUpdate,
    ) -> MovieDescription:
        for field_name, value in movie_in.model_dump(exclude_unset=True).items():
            setattr(movie, field_name, value)
        self.save_state()
        return movie

    def delete_movies(self, slug: str) -> None:
        self.slug_to_movies.pop(slug, None)
        self.save_state()

    def delete(self, movie: MovieDescription) -> None:
        self.delete_movies(slug=movie.slug)


storage = MoviesStorage()
