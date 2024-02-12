"""user models."""

from typing import List
from image import Image

class User():
    """Current user."""

    display_name: str
    user_id: str
    total_follower: int
    country: str
    account_tier: str
    email: str
    images: List[Image]
