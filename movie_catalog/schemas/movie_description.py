import random
from typing import Annotated

from fastapi import Form
from pydantic import BaseModel


class MovieDescriptionBase(BaseModel):
    title: str
    description: str
    genre: list[str]
    release_year: int


class MovieDescriptionCreate(MovieDescriptionBase):
    """
    Модель создания описания фильмов
    """

    slug: Annotated[str, Form()]


class MovieDescriptionUpdate(BaseModel):
    """
    Модель обновления описания фильмов
    """

    title: Annotated[str, Form()]
    description: Annotated[str, Form()]
    genre: Annotated[list[str], Form()]
    release_year: Annotated[int, Form()]


class MovieDescriptionPartialUpdate(MovieDescriptionBase):
    """
    Модель частичного обновления описания фильмов
    """

    title: str | None = None
    description: str | None = None
    genre: list[str] | None = None
    release_year: int | None = None


class MovieDescription(MovieDescriptionBase):
    """
    Модель описания фильмов
    """

    slug: str
