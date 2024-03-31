from pydantic import BaseModel
from datetime import datetime, date


class Image(BaseModel):
    height: int
    width: int
    url: str


class Artist(BaseModel):
    external_urls: dict[str, str]
    href: str
    id: str
    name: str
    type: str
    uri: str


class Album(BaseModel):
    album_type: str
    artists: list[Artist] | list[dict]
    available_markets: list[str]
    external_urls: dict[str, str]
    href: str
    id: str
    images: list[Image]
    name: str
    release_date: date
    release_date_precision: str
    total_tracks: int
    type: str
    uri: str


class Track(BaseModel):
    album: Album
    artists: list[Artist]
    available_markets: list[str]
    disc_number: int
    duration_ms: int
    explicit: bool
    external_ids: dict[str, str]
    external_urls: dict[str, str]
    href: str
    id: str
    is_local: bool
    name: str
    popularity: int
    preview_url: str
    track_number: int
    type: str
    uri: str


class Context(BaseModel):
    type: str
    href: str
    uri: str
    external_urls: dict[str, str]


class TrackRecord(BaseModel):
    track: Track
    played_at: datetime
    context: Context
