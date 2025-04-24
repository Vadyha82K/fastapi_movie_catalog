import random
from typing import Annotated

from fastapi import Form
from pydantic import BaseModel


class MovieDescriptionBase(BaseModel):
    id: int
    title: str
    description: str
    genre: list[str]
    release_year: int


class MovieDescriptionCreate(MovieDescriptionBase):
    """
    Модель создания описания фильмов
    """

    id: int = random.randint(1, 10000)
    title: Annotated[str, Form()]
    description: Annotated[str, Form()]
    genre: Annotated[list[str], Form()]
    release_year: Annotated[int, Form()]


class MovieDescription(MovieDescriptionBase):
    """
    Модель описания фильмов
    """
