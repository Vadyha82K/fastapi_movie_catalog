from unittest import TestCase

from schemas.movie_description import MovieDescription, MovieDescriptionCreate


class MovieDescriptionCreateTestCase(TestCase):
    def test_movie_description_can_be_created_from_create_schema(self) -> None:
        movies_in = MovieDescriptionCreate(
            slug="some-slug",
            title="some-title",
            description="some-description",
            genre=["some-genre", "some-genre"],
            release_year=2025,
        )

        movies = MovieDescription(**movies_in.model_dump())

        self.assertEqual(
            movies_in.slug,
            movies.slug,
        )

        self.assertEqual(
            movies_in.title,
            movies.title,
        )

        self.assertEqual(
            movies_in.description,
            movies.description,
        )

        self.assertEqual(
            movies_in.genre,
            movies.genre,
        )

        self.assertEqual(
            movies_in.release_year,
            movies.release_year,
        )
