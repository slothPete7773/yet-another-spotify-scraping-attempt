"""Track recently played models."""
from pydantic import BaseModel
from .song import Track

class TrackRecentlyPlayed(BaseModel):
    """Tracks recently from User."""

    item: Track
    played_at: str
    type: str
    external_url: str
    captured_type: str
    captured_timestamp: str
