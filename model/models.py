"""Track models."""
# from pydantic import Base
from typing import List, Dict, Optional
from datetime import datetime

from model.base import Base
from dataclasses import dataclass
from dataclasses_json import dataclass_json
import uuid


@dataclass_json
@dataclass
class TrackRecord:
    """Tracks recently from User."""

    track_id: str  # Referential
    played_at: float
    type: Optional[str] = None
    external_url: Optional[Dict[str, str]] = None
    id: str = uuid.uuid4().__str__()


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
class TrackFeature:
    """Artists featured in a track."""

    __tablename__ = "track_feature"

    track_id: str
    artist_id: str
    id: str = uuid.uuid4().__str__()
    createdAt: float = datetime.now().timestamp()


@dataclass_json
@dataclass
class AlbumTrack:
    """A track in the album."""

    __tablename__ = "album_track"

    track_id: str
    album_id: str
    id: str = uuid.uuid4().__str__()
    createdAt: float = datetime.now().timestamp()


@dataclass_json
@dataclass
class Image:
    """Image of a user."""

    __tablename__ = "image"

    url: str
    height: int
    width: int
    id: str = uuid.uuid4().__str__()
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
