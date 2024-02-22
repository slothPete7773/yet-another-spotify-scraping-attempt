"""Track models."""
# from pydantic import Base
from typing import List, Dict
from .image import Image
from .base import Base
from sqlalchemy.orm import DeclarativeBase, Mapped, relationship, mapped_column
from sqlalchemy import ForeignKey
from datetime import datetime

# from datetime import Date


class TrackRecord(Base):
    """Tracks recently from User."""

    id: str
    track_id: str  # Referential
    played_at: datetime
    type: str
    external_url: List[Dict[str, str]]


class Album(Base):
    """Song album"""

    __tablename__ = "album"

    id: str
    external_urls: List[Dict[str, str]]
    href: str
    name: str
    release_date: str
    total_tracks: int


class Artist(Base):
    """Song Artist."""

    __tablename__ = "artist"

    id: str
    external_urls: List[Dict[str, str]]
    href: str
    name: str


class Track(Base):
    """Song track from the Spotify."""

    __tablename__ = "track"

    id: str
    href: str
    name: str
    popularity: int
    preview_url: str
    track_number: int
    external_urls: List[Dict[str, str]]
    # album: Album
    disc_number: int
    duration_ms: int
    explicit: bool
    # artists: List[Artist]
    createdAt: datetime


class TrackFeature(Base):
    """Artists featured in a track."""

    __tablename__ = "track_feature"

    id: str
    track_id: str
    artist_id: str
    createdAt: datetime


class AlbumTrack(Base):
    """A track in the album."""

    __tablename__ = "album_track"

    id: str
    track_id: str
    album_id: str
    createdAt: datetime


class Image(Base):
    """Image of a user."""

    __tablename__ = "image"

    id: str
    url: str
    height: int
    width: int
    ownerId: str


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
