"""Track recently played models."""
from pydantic import BaseModel
from .song import Track
from typing import List, Dict

class TrackRecentlyPlayed(BaseModel):
    """Tracks recently from User."""

    track: Track
    played_at: str
    type: str
    external_url: List[Dict[str, str]]
