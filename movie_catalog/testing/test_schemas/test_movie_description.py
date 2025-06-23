from unittest import TestCase

from pydantic import ValidationError

from schemas.movie_description import (
    MovieDescription,
    MovieDescriptionCreate,
    MovieDescriptionUpdate,
)


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

    def test_movie_description_accepts_different_titles(self) -> None:
        titles = [
            "some title",
            "the one",
            "2015",
            # 2015,
            "The Shawshank Redemption",
        ]

        for title in titles:
            with self.subTest(title=title, msg=f"test-title-{title}"):
                movies_create = MovieDescriptionCreate(
                    slug="some-slug",
                    title=title,
                    description="some-description",
                    genre=["some-genre", "some-genre"],
                    release_year=2025,
                )
                self.assertEqual(title, movies_create.model_dump(mode="json")["title"])

    def test_movie_description_accepts_different_genre(self) -> None:
        genre = [
            [
                "some genre",
                "some genre",
            ],
            # (
            #     "some genre",
            #     "some genre",
            # ),
            # [
            #     "some genre",
            #     34324,
            # ],
            # "Some genre",
            [
                "",
            ],
        ]

        for item in genre:
            with self.subTest(msg=f"test-genre-{item}"):
                movies_create = MovieDescriptionCreate(
                    slug="some-slug",
                    title="some title",
                    description="some-description",
                    genre=item,
                    release_year=2025,
                )
                self.assertEqual(item, movies_create.model_dump(mode="json")["genre"])

    def test_movie_description_accepts_different_release_year(self) -> None:
        release_year = [
            2015,
            0,
            187333457985,
            # "2022",
            # 1.998,
        ]

        for year in release_year:
            with self.subTest(release_year=year, msg=f"test-genre-{year}"):
                movies_create = MovieDescriptionCreate(
                    slug="some-slug",
                    title="some title",
                    description="some-description",
                    genre=[
                        "some genre",
                        "some genre",
                    ],
                    release_year=year,
                )
                self.assertEqual(
                    year,
                    movies_create.model_dump(mode="json")["release_year"],
                )


class MovieDescriptionUpdateTestCase(TestCase):
    def test_movie_description_can_be_updated_from_update_schema(self) -> None:
        movies_in = MovieDescriptionUpdate(
            title="some-title",
            description="some-description",
            genre=["some-genre", "some-genre"],
            release_year=2025,
        )
        movies = MovieDescription(slug="some-slug", **movies_in.model_dump())

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

    def test_movie_description_checking_for_small_slug_length(self) -> None:
        with self.assertRaisesRegex(
            ValidationError,
            expected_regex="String should have at least 3 characters",
        ):
            MovieDescriptionCreate(
                slug="so",
                title="some-title",
                description="some-description",
                genre=["some-genre", "some-genre"],
                release_year=2025,
            )

    def test_movie_description_checking_for_a_longer_slug_length(self) -> None:
        with self.assertRaises(
            ValidationError,
        ) as exc_info:
            MovieDescriptionCreate(
                slug="some slug" * 4,
                title="some-title",
                description="some-description",
                genre=["some-genre", "some-genre"],
                release_year=2025,
            )
        errors_details = exc_info.exception.errors()[0]
        expected_type = "string_too_long"

        self.assertEqual(
            expected_type,
            errors_details["type"],
        )
