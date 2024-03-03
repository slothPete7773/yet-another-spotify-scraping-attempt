import json

# from model.track_recently_played import TrackRecentlyPlayed
from model.models import (
    Album,
    AlbumExternalUrl,
    AlbumImage,
    Artist,
    ArtistExternalUrl,
    Track,
    TrackRecord,
    TrackExternalUrl,
    TrackFeature,
)
from typing import List
import uuid
from datetime import datetime, timedelta

filename = "temp_result.json"

# TODO: iterate through all items
with open(filename, "r") as file:
    content = json.load(file)
    # print(type(content))
    # print(json.dumps(content, indent=2))
    record_activities: list = content["items"]
    # content_item = content[0]

    recently_played = list()

    count = 0
    MAX_ITER = 1
    for record in record_activities:
        if count >= MAX_ITER:
            exit()
        count = count + 1

        track: dict = record["track"]

        album: dict = track["album"]
        # print(album.keys())
        # _album = Album.from_dict(album)
        _album = Album(
            id=album["id"],
            href=album["href"],
            name=album["name"],
            release_date=album["release_date"],
            total_tracks=album["total_tracks"],
            # external_urls="",
        )
        # print(_album)

        _album_images = [
            AlbumImage(
                # id=uuid.uuid4().__str__(),
                url=image["url"],
                width=image["width"],
                height=image["height"],
                album=_album,
            )
            for image in album["images"]
        ]
        # print(_album_images)

        _album_external_urls = [
            AlbumExternalUrl(url=k, source=v, album=_album)
            for k, v in album["external_urls"].items()
        ]
        # print(_album_external_urls)

        artists: list[dict] = track["artists"]
        _artists = list()
        _artists_external_urls = list()

        for artist in artists:
            _artists.append(
                Artist(id=artist["id"], href=artist["href"], name=artist["name"])
            )

            # _artists.append(temp_artist)
            _artists_external_urls.extend(
                [
                    ArtistExternalUrl(source=k, url=v, artist=_artists[-1])
                    for k, v in artist["external_urls"].items()
                ]
            )

        _track = Track(
            href=track["href"],
            name=track["name"],
            popularity=track["popularity"],
            preview_url=track["preview_url"],
            disc_number=track["disc_number"],
            duration_ms=track["duration_ms"],
            track_number=track["track_number"],
            id=track["id"],
            explicit=track["explicit"],
            album=_album,
        )
        # print(_track)

        _track_external_urls = [
            TrackExternalUrl(url=v, source=k, track=_track)
            for k, v in track["external_urls"].items()
        ]
        # print(_track_external_urls)
        _track_feature = [TrackFeature(track=_track, artist=_ao) for _ao in _artists]
        # print(_track_feature)

        _track_record = TrackRecord(
            track=_track,
            played_at=(
                datetime.strptime(
                    record["played_at"].split(".")[0], "%Y-%m-%dT%H:%M:%S"
                )
                + timedelta(hours=7)
            ).timestamp()
            * 1000,
            type=record["context"]["type"] if record["context"] is not None else None,
        )

        print(_track_record)
