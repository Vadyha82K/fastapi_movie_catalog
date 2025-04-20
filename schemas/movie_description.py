from pydantic import BaseModel


class MovieDescriptionBase(BaseModel):
    id: int
    title: str
    description: str
    genre: list[str]
    release_year: int


class MovieDescription(MovieDescriptionBase):
    """
    The movie description model
    """
