"""Track models."""

# from pydantic import Base
from typing import List, Dict, Optional
from datetime import datetime
from dataclasses import dataclass

# from model.base import Base
# from dataclasses import dataclass
# from dataclasses_json import dataclass_json
import uuid

from sqlalchemy.orm import Mapped, relationship, mapped_column, DeclarativeBase
from sqlalchemy import ForeignKey
from sqlalchemy.sql import func


class Base(DeclarativeBase):
    pass


class Album(Base):
    """Song album."""

    __tablename__ = "album"

    id: Mapped[str] = mapped_column(primary_key=True)
    href: Mapped[str]
    name: Mapped[str]
    release_date: Mapped[str]
    total_tracks: Mapped[int]
    # artists: Mapped[List["Artist"]] = relationship(back_populates="album")
    external_urls: Mapped[List["AlbumExternalUrl"]] = relationship(
        back_populates="album"
    )
    included_tracks: Mapped[List["Track"]] = relationship(back_populates="album")
    featured: Mapped[List["AlbumFeaturedArtist"]] = relationship(back_populates="album")
    image: Mapped["AlbumImage"] = relationship(back_populates="album")
    createdAt: Mapped[datetime] = mapped_column(server_default=func.now())

    def __init__(self, **data):
        super().__init__(**data)


class AlbumImage(Base):
    """Cover image of an album."""

    __tablename__ = "album_image"

    url: Mapped[str]
    width: Mapped[int]
    height: Mapped[int]
    id: Mapped[str] = mapped_column(primary_key=True, default=uuid.uuid4().__str__())
    album_id: Mapped[str] = mapped_column(
        ForeignKey("album.id", ondelete="CASCADE", onupdate="CASCADE")
    )
    album: Mapped["Album"] = relationship(back_populates="image")


class AlbumExternalUrl(Base):
    """External url for an album."""

    __tablename__ = "album_external_url"

    url: Mapped[str]
    source: Mapped[str]
    id: Mapped[str] = mapped_column(primary_key=True, default=uuid.uuid4().__str__())
    album: Mapped["Album"] = relationship(back_populates="external_urls")
    album_id: Mapped[str] = mapped_column(
        ForeignKey("album.id", ondelete="CASCADE", onupdate="CASCADE")
    )
    createdAt: Mapped[datetime] = mapped_column(server_default=func.now())


class Artist(Base):
    """Song Artist."""

    __tablename__ = "artist"

    id: Mapped[str] = mapped_column(primary_key=True)
    href: Mapped[str]
    name: Mapped[str]
    external_urls: Mapped[List["ArtistExternalUrl"]] = relationship(
        back_populates="artist"
    )
    # album: Mapped[List["Album"]] = relationship(back_populates="artist")
    featured: Mapped[List["TrackFeature"]] = relationship(back_populates="artist")
    album_featured: Mapped[List["AlbumFeaturedArtist"]] = relationship(
        back_populates="artist"
    )
    createdAt: Mapped[datetime] = mapped_column(server_default=func.now())


class ArtistExternalUrl(Base):
    """External url for an album."""

    __tablename__ = "artist_external_url"

    url: Mapped[str]
    source: Mapped[str]
    id: Mapped[str] = mapped_column(primary_key=True, default=uuid.uuid4().__str__())
    artist: Mapped["Artist"] = relationship(back_populates="external_urls")
    artist_id: Mapped[str] = mapped_column(
        ForeignKey("artist.id", ondelete="CASCADE", onupdate="CASCADE")
    )
    createdAt: Mapped[datetime] = mapped_column(server_default=func.now())


class AlbumFeaturedArtist(Base):
    """The Artists featured in corresponding Album."""

    __tablename__ = "album_featured_artist"

    id: Mapped[str] = mapped_column(primary_key=True, default=uuid.uuid4().__str__())
    album_id: Mapped[str] = mapped_column(
        ForeignKey("album.id", ondelete="CASCADE", onupdate="CASCADE")
    )
    album: Mapped["Album"] = relationship(back_populates="featured")
    artist_id: Mapped[str] = mapped_column(
        ForeignKey("artist.id", ondelete="CASCADE", onupdate="CASCADE")
    )
    artist: Mapped["Artist"] = relationship(back_populates="album_featured")
    createdAt: Mapped[datetime] = mapped_column(server_default=func.now())


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
    album_id: Mapped[str] = mapped_column(
        ForeignKey("album.id", ondelete="CASCADE", onupdate="CASCADE"),
    )
    album: Mapped[Optional["Album"]] = relationship(back_populates="included_tracks")
    external_urls: Mapped[List["TrackExternalUrl"]] = relationship(
        back_populates="track"
    )
    featured: Mapped[List["TrackFeature"]] = relationship(back_populates="track")
    createdAt: Mapped[datetime] = mapped_column(server_default=func.now())

    def __repr__(self):
        return f"<Track(id='{self.id}', name='{self.name}')>"


class TrackExternalUrl(Base):
    """External url for an album."""

    __tablename__ = "track_external_url"

    url: Mapped[str]
    source: Mapped[str]
    id: Mapped[str] = mapped_column(primary_key=True, default=uuid.uuid4().__str__())
    track: Mapped["Track"] = relationship(back_populates="external_urls")
    track_id: Mapped[str] = mapped_column(
        ForeignKey("track.id", ondelete="CASCADE", onupdate="CASCADE")
    )
    createdAt: Mapped[datetime] = mapped_column(server_default=func.now())


class TrackFeature(Base):
    """Artists featured in a track."""

    __tablename__ = "track_feature"

    id: Mapped[str] = mapped_column(primary_key=True, default=uuid.uuid4().__str__())
    track_id: Mapped[str] = mapped_column(
        ForeignKey("track.id", ondelete="CASCADE", onupdate="CASCADE")
    )
    track: Mapped["Track"] = relationship(back_populates="featured")
    artist_id: Mapped[str] = mapped_column(
        ForeignKey("artist.id", ondelete="CASCADE", onupdate="CASCADE")
    )
    artist: Mapped["Artist"] = relationship(back_populates="featured")
    createdAt: Mapped[datetime] = mapped_column(server_default=func.now())


class TrackRecord(Base):
    """Tracks recently from User."""

    __tablename__ = "track_record"

    id: Mapped[str] = mapped_column(primary_key=True, default=uuid.uuid4().__str__())
    track_id: Mapped[str] = mapped_column(
        ForeignKey("track.id", ondelete="CASCADE", onupdate="CASCADE")
    )
    track: Mapped["Track"] = relationship()
    type: Mapped[Optional[str]]
    createdAt: Mapped[datetime] = mapped_column(server_default=func.now())
    played_at: Mapped[float]

    def __repr__(self):
        return f"<TrackRecord(id='{self.id}', track_id='{self.track_id}', track='{self.track}', played_at='{self.played_at}', type='{self.type}')>"


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
