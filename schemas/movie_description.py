from pydantic import BaseModel


class MovieDescriptionBase(BaseModel):
    id: int
    title: str
    description: str


class MovieDescription(MovieDescriptionBase):
    """
    The movie description model
    """
