import json
from model.track_recently_played import TrackRecentlyPlayed
from model.song import Track, Album, Artist
from typing import List

filename = "temp_result.json"

# TODO: iterate through all items
with open(filename, 'r') as file:
    content = json.load(file)
    # print(type(content))
    # print(json.dumps(content, indent=2))
    content = content['items']
    content_item = content[0]
    content_track = content_item['track']
    
    content_album = content_track['album']
    album: Album = Album(
        id=content_album['id'],
        external_urls=list(map(lambda name, url: {name: url}, content_album['external_urls'].keys(), content_album['external_urls'].values())),
        href=content_album['href'],
        name=content_album['name'],
        release_date=content_album['release_date'],
        total_tracks=content_album['total_tracks'],
        images=content_album['images'],
    )
    # print(album.model_dump_json(indent=2))
    
    content_artists = content_track['artists']
    artists: List[Artist] = [Artist(
        id=artist['id'],
        external_urls=list(map(lambda name, url: {name: url}, artist['external_urls'].keys(), artist['external_urls'].values())),
        href=artist['href'],
        name=artist['name'],
    ) for artist in content_track['artists']]
    # print(artists)
    

    track: Track = Track(
        id=content_track['id'],
        href=content_track['href'],
        name=content_track['name'],
        popularity=content_track['popularity'],
        preview_url=content_track['preview_url'],
        track_number=content_track['track_number'],
        external_urls=map(lambda name, url: {name: url}, content_track['external_urls'].keys(), content_track['external_urls'].values()),
        # list(map(lambda name, url: {name: url}, dic['external_urls'].keys(), dic['external_urls'].values()))
        album=album,
        disc_number=content_track['disc_number'],
        duration_ms=content_track['duration_ms'],
        explicit=content_track['explicit'],
        artists=artists,
    )
    # print(track.model_dump_json(indent=2))


    recently_played = TrackRecentlyPlayed(
        item=track,
        played_at=content_item["played_at"],
        type=content_item["context"]["type"],
        external_url=list(map(lambda name, url: {name: url}, content_item["context"]['external_urls'].keys(), content_item["context"]['external_urls'].values())),
    )
    print(recently_played.model_dump_json(indent=2))
    