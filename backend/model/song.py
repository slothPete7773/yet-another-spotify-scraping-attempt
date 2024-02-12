"""Track models."""

from typing import List, Dict
from image import Image
# from datetime import Date

class Album: 
    """Song album"""
    id: str
    external_url: str
    href: str
    name: str
    release_date: str
    total_tracks: int
    images: List[Image]

class Artist:
    """Song Artist"""
    id: str
    external_url: str
    href: str
    name: str
    

class Track:
    """Song track from the Spotify"""

    id: str
    href: str
    name: str
    popularity: int
    preview_url: str
    track_number: int
    external_urls: List[Dict[str, str]]
    album: Album
    disc_number: int
    duration: int
    explicit: bool
    artists: List[Artist]