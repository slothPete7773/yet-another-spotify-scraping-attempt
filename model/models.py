"""Track models."""
# from pydantic import Base
from typing import List, Dict, Optional
from datetime import datetime

from .base import Base
from dataclasses import dataclass
from dataclasses_json import dataclass_json


@dataclass_json
@dataclass
class TrackRecord:
    """Tracks recently from User."""

    id: str
    track_id: str  # Referential
    played_at: float
    type: Optional[str] = None
    external_url: Optional[Dict[str, str]] = None


@dataclass_json
@dataclass
class Album(Base):
    """Song album"""

    __tablename__ = "album"

    id: str
    external_urls: Dict[str, str]
    href: str
    name: str
    release_date: str
    total_tracks: int

    def __init__(self, **data):
        super().__init__(**data)


@dataclass_json
@dataclass
class Artist(Base):
    """Song Artist."""

    __tablename__ = "artist"

    id: str
    external_urls: Dict[str, str]
    href: str
    name: str

    def __init__(self, **data):
        super().__init__(**data)


@dataclass_json
@dataclass
class Track:
    """Song track from the Spotify."""

    __tablename__ = "track"

    id: str
    href: str
    name: str
    popularity: int
    preview_url: str
    track_number: int
    external_urls: Dict[str, str]
    # album: Album
    disc_number: int
    duration_ms: int
    explicit: bool
    # artists: List[Artist]
    # createdAt: Optional[float] = datetime.now().timestamp
    createdAt: float = datetime.now().timestamp()

    # def __init__(self, **data):
    #     super().__init__(**data)


@dataclass_json
@dataclass
class TrackFeature(Base):
    """Artists featured in a track."""

    __tablename__ = "track_feature"

    id: str
    track_id: str
    artist_id: str
    createdAt: float


@dataclass_json
@dataclass
class AlbumTrack(Base):
    """A track in the album."""

    __tablename__ = "album_track"

    id: str
    track_id: str
    album_id: str
    createdAt: float


@dataclass_json
@dataclass
class Image(Base):
    """Image of a user."""

    __tablename__ = "image"

    id: str
    url: str
    height: int
    width: int
    ownerId: str = None


@dataclass_json
@dataclass
class User(Base):
    """Current user."""

    __tablename__ = "user"

    id: str
    display_name: str
    user_id: str
    total_follower: int
    country: str
    account_tier: str
    email: str
    # image_id: Optional[List

    # images: List[Image] = relationship()
