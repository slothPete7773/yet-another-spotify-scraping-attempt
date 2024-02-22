import json

# from model.track_recently_played import TrackRecentlyPlayed
from model.models import Track, Album, Artist, TrackRecord
from typing import List

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
        print(_artists)
        # print(artists)

        # TODO: To continue change implementation.
        track: Track = Track(
            id=track["id"],
            href=track["href"],
            name=track["name"],
            popularity=track["popularity"],
            preview_url=track["preview_url"],
            track_number=track["track_number"],
            external_urls=map(
                lambda name, url: {name: url},
                track["external_urls"].keys(),
                track["external_urls"].values(),
            ),
            # list(map(lambda name, url: {name: url}, dic['external_urls'].keys(), dic['external_urls'].values()))
            album=album,
            disc_number=track["disc_number"],
            duration_ms=track["duration_ms"],
            explicit=track["explicit"],
            artists=artists,
        )
        # print(track.model_dump_json(indent=2))

        recently_played.append(
            TrackRecord(
                track=track,
                played_at=record["played_at"],
                type=record["context"]["type"],
                external_url=list(
                    map(
                        lambda name, url: {name: url},
                        record["context"]["external_urls"].keys(),
                        record["context"]["external_urls"].values(),
                    )
                ),
            ).model_dump()
        )

        # result = recently_played.model_dump_json(indent=2)
        # print(type(result))
    # result = recently_played.model_dump()
    with open("result_result.json", "w") as file:
        json.dump(recently_played, file, indent=2)
