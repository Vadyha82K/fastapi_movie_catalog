import random
from collections.abc import Generator
from string import ascii_letters
from typing import ClassVar
from unittest import TestCase

import pytest

from api.api_v1.movies.crud import (
    MovieAlreadyExistsError,
    storage,
)
from schemas.movie_description import (
    MovieDescription,
    MovieDescriptionCreate,
    MovieDescriptionPartialUpdate,
    MovieDescriptionUpdate,
)


def create_movie() -> MovieDescription:
    movie_in = MovieDescriptionCreate(
        slug="".join(random.choices(ascii_letters, k=8)),  # noqa: S311
        title="some title",
        description="some description",
        genre=["some genre", "some genre"],
        release_year=2025,
    )
    return storage.create_movies(movie_in)


@pytest.fixture
def movies() -> Generator[MovieDescription]:
    movies = create_movie()
    yield movies
    storage.delete(movies)


class MovieDescriptionUpdateTestCase(TestCase):
    def setUp(self) -> None:
        self.movies = create_movie()

    def tearDown(self) -> None:
        storage.delete(self.movies)

    def test_update(self) -> None:
        movies_update = MovieDescriptionUpdate(
            **self.movies.model_dump(),
        )
        source_description = self.movies.description
        movies_update.description *= 2
        updated_movies = storage.update(
            movie=self.movies,
            movie_in=movies_update,
        )
        self.assertNotEqual(
            source_description,
            updated_movies.description,
        )
        self.assertEqual(
            movies_update,
            MovieDescriptionUpdate(**updated_movies.model_dump()),
        )

    def test_update_partial(self) -> None:
        movies_update_partial = MovieDescriptionPartialUpdate(
            description=self.movies.description * 2,
        )
        source_description = self.movies.description
        updated_movies = storage.update_partial(
            movie=self.movies,
            movie_in=movies_update_partial,
        )
        self.assertNotEqual(
            source_description,
            updated_movies.description,
        )
        self.assertEqual(
            movies_update_partial.description,
            updated_movies.description,
        )


class MovieDescriptionUpdateGetMoviesTestCase(TestCase):
    MOVIES_COUNTS = 3
    movies: ClassVar[list[MovieDescription]] = []

    @classmethod
    def setUpClass(cls) -> None:
        cls.movies = [create_movie() for _ in range(cls.MOVIES_COUNTS)]

    @classmethod
    def tearDownClass(cls) -> None:
        for movie in cls.movies:
            storage.delete(movie)

    def test_get_list(self) -> None:
        movies_desc = storage.get_list_movies()
        expected_slug = {mov.slug for mov in self.movies}
        slugs = {mov.slug for mov in movies_desc}
        expected_diff = set[str]()
        diff = expected_slug - slugs
        self.assertEqual(expected_diff, diff)

    def test_get_by_slug(self) -> None:
        for movie in self.movies:
            with self.subTest(
                slug=movie.slug,
                msg=f"Validate can get slug {movie.slug!r}",
            ):
                db_movies = storage.get_movies_by_slug(movie.slug)
                self.assertEqual(
                    movie,
                    db_movies,
                )


def test_create_or_raise_if_exists(movies: MovieDescription) -> None:
    movies_create = MovieDescriptionCreate(**movies.model_dump())
    with pytest.raises(
        MovieAlreadyExistsError,
        match=movies_create.slug,
    ) as exc_info:
        storage.create_or_raise_if_exists(movies_create)
    assert exc_info.value.args[0] == movies_create.slug
