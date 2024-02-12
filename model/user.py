"""user models."""
from pydantic import BaseModel
from typing import List
from .image import Image

class User(BaseModel):
    """Current user."""

    display_name: str
    user_id: str
    total_follower: int
    country: str
    account_tier: str
    email: str
    images: List[Image]
