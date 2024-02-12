"""image models."""
from pydantic import BaseModel

class Image(BaseModel):
    """Image of a user."""

    url: str
    height: int
    width: int