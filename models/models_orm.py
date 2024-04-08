"""Track models."""

from typing import List, Dict, Optional

from datetime import datetime, date
from dataclasses import dataclass

import uuid

from sqlalchemy.orm import Mapped, relationship, mapped_column, DeclarativeBase
from sqlalchemy import ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.types import DateTime


class Base(DeclarativeBase):
    pass


class AlbumORM(Base):
    """Song album."""

    __tablename__ = "album"

    id: Mapped[str] = mapped_column(primary_key=True)
    href: Mapped[str]
    name: Mapped[str]
    release_date: Mapped[date]
    total_tracks: Mapped[int]
    # artists: Mapped[List["Artist"]] = relationship(back_populates="album")
    external_urls: Mapped[List["AlbumExternalUrlORM"]] = relationship(
        back_populates="album"
    )
    image: Mapped["AlbumImageORM"] = relationship(back_populates="album")
    createdAt: Mapped[datetime] = mapped_column(server_default=func.now())

    def __init__(self, **data):
        super().__init__(**data)


class AlbumImageORM(Base):
    """Cover image of an album."""

    __tablename__ = "album_image"

    url: Mapped[str]
    width: Mapped[int]
    height: Mapped[int]
    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True, default=uuid.uuid4, unique=True
    )
    album_id: Mapped[str] = mapped_column(
        ForeignKey("album.id", ondelete="CASCADE", onupdate="CASCADE")
    )
    album: Mapped["AlbumORM"] = relationship(back_populates="image")

    def __repr__(self) -> str:
        return f"AlbumImageORM(url='{self.url}', width='{self.width}', height='{self.height}', id='{self.id}', album_id='{self.album_id}'), album='{self.album}'"


class AlbumExternalUrlORM(Base):
    """External url for an album."""

    __tablename__ = "album_external_url"

    url: Mapped[str]
    source: Mapped[str]
    id: Mapped[str] = mapped_column(primary_key=True, default=uuid.uuid4)
    album: Mapped["AlbumORM"] = relationship(back_populates="external_urls")
    album_id: Mapped[str] = mapped_column(
        ForeignKey("album.id", ondelete="CASCADE", onupdate="CASCADE")
    )
    createdAt: Mapped[datetime] = mapped_column(server_default=func.now())


class ArtistORM(Base):
    """Song Artist."""

    __tablename__ = "artist"

    id: Mapped[str] = mapped_column(primary_key=True)
    href: Mapped[str]
    name: Mapped[str]
    external_urls: Mapped[List["ArtistExternalUrlORM"]] = relationship(
        back_populates="artist"
    )
    featured: Mapped[List["TrackFeatureORM"]] = relationship(back_populates="artist")
    createdAt: Mapped[datetime] = mapped_column(server_default=func.now())


class ArtistExternalUrlORM(Base):
    """External url for an album."""

    __tablename__ = "artist_external_url"

    url: Mapped[str]
    source: Mapped[str]
    id: Mapped[str] = mapped_column(primary_key=True, default=uuid.uuid4)
    artist: Mapped["ArtistORM"] = relationship(back_populates="external_urls")
    artist_id: Mapped[str] = mapped_column(
        ForeignKey("artist.id", ondelete="CASCADE", onupdate="CASCADE")
    )
    createdAt: Mapped[datetime] = mapped_column(server_default=func.now())


class TrackORM(Base):
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
    album_id: Mapped[str] = mapped_column(
        ForeignKey("album.id", ondelete="CASCADE", onupdate="CASCADE"),
    )
    external_urls: Mapped[List["TrackExternalUrlORM"]] = relationship(
        back_populates="track"
    )
    featured: Mapped[List["TrackFeatureORM"]] = relationship(back_populates="track")
    createdAt: Mapped[datetime] = mapped_column(server_default=func.now())

    def __repr__(self):
        return f"<Track(id='{self.id}', name='{self.name}')>"


class TrackExternalUrlORM(Base):
    """External url for an album."""

    __tablename__ = "track_external_url"

    url: Mapped[str]
    source: Mapped[str]
    id: Mapped[str] = mapped_column(primary_key=True, default=uuid.uuid4)
    track: Mapped["TrackORM"] = relationship(back_populates="external_urls")
    track_id: Mapped[str] = mapped_column(
        ForeignKey("track.id", ondelete="CASCADE", onupdate="CASCADE")
    )
    createdAt: Mapped[datetime] = mapped_column(server_default=func.now())

    def __repr__(self):
        return f"TrackExternalUrlORM(url='{self.url}', source='{self.source}', id='{self.id}', track='{self.track}', track_id='{self.track_id}', createdAt='{self.createdAt}')"


class TrackFeatureORM(Base):
    """Artists featured in a track."""

    __tablename__ = "track_feature"

    id: Mapped[str] = mapped_column(primary_key=True, default=uuid.uuid4)
    track_id: Mapped[str] = mapped_column(
        ForeignKey("track.id", ondelete="CASCADE", onupdate="CASCADE")
    )
    track: Mapped["TrackORM"] = relationship(back_populates="featured")
    artist_id: Mapped[str] = mapped_column(
        ForeignKey("artist.id", ondelete="CASCADE", onupdate="CASCADE")
    )
    artist: Mapped["ArtistORM"] = relationship(back_populates="featured")
    createdAt: Mapped[datetime] = mapped_column(server_default=func.now())


class TrackRecordORM(Base):
    """Tracks recently from User."""

    __tablename__ = "track_record"

    id: Mapped[str] = mapped_column(primary_key=True, default=uuid.uuid4)
    track_id: Mapped[str] = mapped_column(
        ForeignKey("track.id", ondelete="CASCADE", onupdate="CASCADE")
    )
    track: Mapped["TrackORM"] = relationship()
    type: Mapped[Optional[str]]
    createdAt: Mapped[datetime] = mapped_column(server_default=func.now())
    played_at: Mapped[datetime]

    def __repr__(self):
        return f"<TrackRecord(id='{self.id}', track_id='{self.track_id}', track='{self.track}', played_at='{self.played_at}', type='{self.type}')>"


class UserORM(Base):
    """Current user."""

    __tablename__ = "user"

    email: Mapped[str]
    user_id: Mapped[str]
    total_follower: Mapped[int]
    country: Mapped[str]
    account_tier: Mapped[str]
    display_name: Mapped[str]
    id: Mapped[str] = mapped_column(primary_key=True, default=uuid.uuid4)
