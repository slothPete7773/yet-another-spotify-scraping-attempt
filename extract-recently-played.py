import json

# from model.track_recently_played import TrackRecentlyPlayed
from model.models import Track, Album, Artist, TrackRecord
from typing import List
import uuid
from datetime import datetime

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
    MAX_ITER = 3
    for record in record_activities:
        if count >= MAX_ITER:
            exit()
        count = count + 1

        track: dict = record["track"]

        album: dict = track["album"]
        # print(album.keys())
        _album = Album.from_dict(album)

        artists: list[dict] = track["artists"]
        _artists = [Artist.from_dict(artist) for artist in artists]
        # print(_artists)

        _track = Track.from_dict(track)

        # print(record)
        _temp = {
            "id": uuid.uuid4().__str__(),
            "track_id": _track.id,
            "played_at": datetime.strptime(
                record["played_at"].split(".")[0], "%Y-%m-%dT%H:%M:%S"
            ).timestamp(),
            "type": record["context"]["type"]
            if record["context"] is not None
            else None,
            "external_url": record["context"]["external_urls"]
            if record["context"] is not None
            else None,
        }

        _track_record = TrackRecord.from_dict(_temp)
        # print(_track_record)
