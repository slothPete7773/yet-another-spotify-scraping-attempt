import json
from model.track_recently_played import TrackRecentlyPlayed
from model.song import Track, Album, Artist
from typing import List

filename = "temp_result.json"

with open(filename, 'r') as file:
    content = json.load(file)
    # print(type(content))
    # print(json.dumps(content, indent=2))
    content = content['items']
    content_track = content[0]['track']
    
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
    
    # content_artists = content_track['artists']
    # artists: List[Artist] = [Artist(
    #     id=artist['id'],
    #     external_urls=list(map(lambda name, url: {name: url}, artist['external_urls'].keys(), artist['external_urls'].values())),
    #     href=artist['href'],
    #     name=artist['name'],
    # ) for artist in content_track['artists']]
    # print(artists)
    

    # track: Track = Track(
    #     id=content_track['id'],
    #     href=content_track['href'],
    #     name=content_track['name'],
    #     popularity=content_track['popularity'],
    #     preview_url=content_track['preview_url'],
    #     track_number=content_track['track_number'],
    #     external_urls=map(lambda name, url: {name: url}, content_track['external_urls'].keys(), content_track['external_urls'].values()),
    #     # list(map(lambda name, url: {name: url}, dic['external_urls'].keys(), dic['external_urls'].values()))
    #     album=album,
    #     disc_number=content_track['disc_number'],
    #     duration=content_track['duration'],
    #     explicit=content_track['explicit'],
    #     artists=artists,
    # )
    # TrackRecentlyPlayed()
    
    # for i in content[0].keys():
    #     print(i)