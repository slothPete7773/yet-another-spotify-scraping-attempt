from pydantic import BaseModel
from app.models.domain.artist import Artist
from app.models.domain.image import Image


class Album(BaseModel):
    album_type: str
    artists: list[Artist] | list[dict]
    # available_markets: list[str]
    # external_urls: dict[str, str]
    # href: str
    # id: str
    # images: list[Image]
    # name: str
    # release_date: str
    # release_date_precision: str
    # total_tracks: int
    # type: str
    # uri: str
