from typing import Union
from pydantic import BaseModel
from app.models.domain.artist import Artist
from app.models.domain.image import Image
from app.models.common import AuditLogModelAttribute, IDModelAttribute


class Album(BaseModel, AuditLogModelAttribute, IDModelAttribute):
    album_type: str
    artists: list[Artist]  # | list[dict] # Cannot remember why allow `list[dict]`
    available_markets: list[str]
    external_urls: dict[str, str]
    href: str
    images: list[Image]
    name: str
    release_date: str
    release_date_precision: str
    total_tracks: int
    type: str
    uri: str
