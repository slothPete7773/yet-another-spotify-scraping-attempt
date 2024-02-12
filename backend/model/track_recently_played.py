"""Track recently played models."""

from song import Track

class TrackRecentlyPlayed:
    """Tracks recently from User."""

    item: Track
    played_at: str
    type: str
    external_url: str
    captured_type: str
    captured_timestamp: str
