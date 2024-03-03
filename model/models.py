"""Track models."""
# from pydantic import Base
from typing import List, Dict, Optional
from datetime import datetime

from model.base import Base
from dataclasses import dataclass
from dataclasses_json import dataclass_json
import uuid

from sqlalchemy.orm import Mapped, relationship, mapped_column
from sqlalchemy import ForeignKey
from sqlalchemy.sql import func


@dataclass_json
@dataclass
class Album(Base):
    """Song album."""

    __tablename__ = "album"

    id: Mapped[str] = mapped_column(primary_key=True)
    href: Mapped[str]
    name: Mapped[str]
    release_date: Mapped[str]
    total_tracks: Mapped[int]
    external_urls: Mapped[List["AlbumExternalUrl"]] = relationship(
        back_populates="album"
    )
    included_tracks: Mapped[List["Track"]] = relationship(back_populates="album")

    image: Mapped["AlbumImage"] = relationship(back_populates="album")
    createdAt: Mapped[datetime] = mapped_column(server_default=func.now())

    def __init__(self, **data):
        super().__init__(**data)


@dataclass_json
@dataclass
class AlbumImage(Base):
    """Cover image of an album."""

    __tablename__ = "album_image"

    url: Mapped[str]
    width: Mapped[int]
    height: Mapped[int]
    id: Mapped[str] = mapped_column(primary_key=True, default=uuid.uuid4().__str__())
    album_id: Mapped[str] = mapped_column(ForeignKey("album.id"))
    album: Mapped["Album"] = relationship(back_populates="image")


@dataclass_json
@dataclass
class AlbumExternalUrl(Base):
    """External url for an album."""

    __tablename__ = "album_external_url"

    url: Mapped[str]
    source: Mapped[str]
    id: Mapped[str] = mapped_column(primary_key=True, default=uuid.uuid4().__str__())
    album: Mapped["Album"] = relationship(back_populates="external_urls")
    album_id: Mapped[str] = mapped_column(ForeignKey("album.id"))
    createdAt: Mapped[datetime] = mapped_column(server_default=func.now())


@dataclass_json
@dataclass
class Artist(Base):
    """Song Artist."""

    __tablename__ = "artist"

    id: Mapped[str] = mapped_column(primary_key=True)
    href: Mapped[str]
    name: Mapped[str]
    external_urls: Mapped[List["ArtistExternalUrl"]] = relationship(
        back_populates="artist"
    )
    featured: Mapped[List["TrackFeature"]] = relationship(back_populates="artist")
    createdAt: Mapped[datetime] = mapped_column(server_default=func.now())


@dataclass_json
@dataclass
class ArtistExternalUrl(Base):
    """External url for an album."""

    __tablename__ = "artist_external_url"

    url: Mapped[str]
    source: Mapped[str]
    id: Mapped[str] = mapped_column(primary_key=True, default=uuid.uuid4().__str__())
    artist: Mapped["Artist"] = relationship(back_populates="external_urls")
    artist_id: Mapped[str] = mapped_column(ForeignKey("artist.id"))
    createdAt: Mapped[datetime] = mapped_column(server_default=func.now())


@dataclass_json
@dataclass
class Track(Base):
    """Song track from the Spotify."""

    __tablename__ = "track"

    href: Mapped[str]
    name: Mapped[str]
    popularity: Mapped[int]
    preview_url: Mapped[str]
    disc_number: Mapped[int]
    duration_ms: Mapped[int]
    track_number: Mapped[int]
    id: Mapped[str] = mapped_column(primary_key=True)
    explicit: Mapped[bool] = mapped_column(default=False)
    album_id: Mapped[str] = mapped_column(ForeignKey("album.id"))
    album: Mapped["Album"] = relationship(back_populates="included_tracks")
    external_urls: Mapped[List["TrackExternalUrl"]] = relationship(
        back_populates="track"
    )
    featured: Mapped[List["TrackFeature"]] = relationship(back_populates="track")
    createdAt: Mapped[datetime] = mapped_column(server_default=func.now())

    def __repr__(self):
        return f"<Track(id='{self.id}', name='{self.name}')>"


@dataclass_json
@dataclass
class TrackExternalUrl(Base):
    """External url for an album."""

    __tablename__ = "track_external_url"

    url: Mapped[str]
    source: Mapped[str]
    id: Mapped[str] = mapped_column(primary_key=True, default=uuid.uuid4().__str__())
    track: Mapped["Track"] = relationship(back_populates="external_urls")
    track_id: Mapped[str] = mapped_column(ForeignKey("track.id"))
    createdAt: Mapped[datetime] = mapped_column(server_default=func.now())


@dataclass_json
@dataclass
class TrackFeature(Base):
    """Artists featured in a track."""

    __tablename__ = "track_feature"

    id: Mapped[str] = mapped_column(primary_key=True, default=uuid.uuid4().__str__())
    track_id: Mapped[str] = mapped_column(ForeignKey("track.id"))
    track: Mapped["Track"] = relationship(back_populates="featured")
    artist_id: Mapped[str] = mapped_column(ForeignKey("artist.id"))
    artist: Mapped["Artist"] = relationship(back_populates="featured")
    createdAt: Mapped[datetime] = mapped_column(server_default=func.now())


@dataclass_json
@dataclass
class TrackRecord(Base):
    """Tracks recently from User."""

    __tablename__ = "track_record"

    track_id: Mapped[str] = mapped_column(ForeignKey("track.id"))  # Referential
    track: Mapped["Track"] = relationship()
    played_at: Mapped[float]
    id: Mapped[str] = mapped_column(primary_key=True, default=uuid.uuid4().__str__())
    type: Mapped[Optional[str]] = None
    createdAt: Mapped[datetime] = mapped_column(server_default=func.now())

    def __repr__(self):
        return f"<TrackRecord(id='{self.id}', track_id='{self.track_id}', track='{self.track}', played_at='{self.played_at}', type='{self.type}')>"


@dataclass_json
@dataclass
class User(Base):
    """Current user."""

    __tablename__ = "user"

    email: Mapped[str]
    user_id: Mapped[str]
    total_follower: Mapped[int]
    country: Mapped[str]
    account_tier: Mapped[str]
    display_name: Mapped[str]
    id: Mapped[str] = mapped_column(primary_key=True, default=uuid.uuid4().__str__())
