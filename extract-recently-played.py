import json
from datetime import datetime

from models.models_orm import (
    AlbumORM,
    AlbumImageORM,
    AlbumExternalUrlORM,
    ArtistORM,
    ArtistExternalUrlORM,
    TrackORM,
    TrackExternalUrlORM,
    TrackFeatureORM,
    TrackRecordORM,
    UserORM,
    # Session,
)
from models.models import *

from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.orm.exc import NoResultFound

filename = "test_file.json"

pg_uri = "postgresql://postgres:example@localhost:8032/postgres"
engine = create_engine(pg_uri, echo=True)


def get_or_create(session, model, **kwargs):
    instance = get_instance(session, model, **kwargs)
    if instance is None:
        instance = create_instance(session, model, **kwargs)

    return instance


def get_instance(session, model, **kwargs):
    try:
        return session.query(model).filter_by(**kwargs).first()
    except NoResultFound:
        return


def create_instance(session, model, **kwargs):
    try:
        instance = model(**kwargs)
        session.add(instance)
        session.flush()
    except Exception as msg:
        # mtext = 'model:{}, args:{} => msg:{}'
        # log.error(mtext.format(model, kwargs, msg))
        session.rollback()
        raise (msg)
    return instance


with Session(engine) as session:

    with open(filename, "r") as file:
        content = json.load(file)
        recorded_activities: list = content["items"]

        recently_played = list()

        count = 0
        MAX_ITERATION = 1

        for record in recorded_activities:

            activity: TrackRecord = TrackRecord(**record)

            # Album
            album_item: Album = activity.track.album
            album_orm: AlbumORM = get_or_create(
                session,
                AlbumORM,
                id=album_item.id,
                href=album_item.href,
                name=album_item.name,
                release_date=album_item.release_date,
                total_tracks=album_item.total_tracks,
            )
            # album_orm: AlbumORM = AlbumORM(
            #     id=album_item.id,
            #     href=album_item.href,
            #     name=album_item.name,
            #     release_date=album_item.release_date,
            #     total_tracks=album_item.total_tracks,
            # )

            # Track
            track_item: Track = activity.track
            track_orm = get_or_create(
                session,
                TrackORM,
                href=track_item.href,
                name=track_item.name,
                popularity=track_item.popularity,
                preview_url=track_item.preview_url,
                disc_number=track_item.disc_number,
                duration_ms=track_item.duration_ms,
                track_number=track_item.track_number,
                id=track_item.id,
                explicit=track_item.explicit,
                album_id=track_item.album.id,
            )
            # track_orm: TrackORM = TrackORM(
            #     href=track_item.href,
            #     name=track_item.name,
            #     popularity=track_item.popularity,
            #     preview_url=track_item.preview_url,
            #     disc_number=track_item.disc_number,
            #     duration_ms=track_item.duration_ms,
            #     track_number=track_item.track_number,
            #     id=track_item.id,
            #     explicit=track_item.explicit,
            #     album_id=track_item.album.id,
            # )

            # Artist
            track_artist_items = track_item.artists
            artists_coll = []
            track_features_coll = []
            for artist in track_artist_items:
                artist_orm: ArtistORM = get_or_create(
                    session,
                    ArtistORM,
                    id=artist.id,
                    href=artist.href,
                    name=artist.name,
                )
                # artist_orm: ArtistORM = ArtistORM(
                #     id=artist.id,
                #     href=artist.href,
                #     name=artist.name,
                # )
                artists_coll.append(artist_orm)

                track_feature_orm: TrackFeatureORM = get_or_create(
                    session,
                    TrackFeatureORM,
                    track=track_orm,
                    artist=artist_orm,
                )
                # track_feature_orm: TrackFeatureORM = TrackFeatureORM(
                #     track=track_orm,
                #     artist=artist_orm,
                # )
                track_features_coll.append(track_feature_orm)

                # session.add(artist_orm)
                # session.add(track_feature_orm)

            # External URLs
            track_external_urls_coll = []
            for url_key, url_value in track_item.external_urls.items():
                track_external_url_orm: TrackExternalUrlORM = get_or_create(
                    session,
                    TrackExternalUrlORM,
                    url=url_key,
                    source=url_value,
                    track=track_orm,
                )
                # track_external_url_orm: TrackExternalUrlORM = TrackExternalUrlORM(
                #     url=url_key,
                #     source=url_value,
                #     track=track_orm,
                # )
                # session.add(track_external_url_orm)
                track_external_urls_coll.append(track_external_url_orm)

            artist_external_urls_coll = []
            for url_key, url_value in artist.external_urls.items():

                artist_external_url_orm: ArtistExternalUrlORM = get_or_create(
                    session,
                    ArtistExternalUrlORM,
                    url=url_key,
                    source=url_value,
                    artist=artist_orm,
                )
                # artist_external_url_orm: ArtistExternalUrlORM = ArtistExternalUrlORM(
                #     url=url_key,
                #     source=url_value,
                #     artist=artist_orm,
                # )
                # session.add(artist_external_url_orm)
                artist_external_urls_coll.append(artist_external_url_orm)

            album_external_urls_coll = []
            for url_key, url_value in album_item.external_urls.items():

                album_external_url_orm: AlbumExternalUrlORM = get_or_create(
                    session,
                    AlbumExternalUrlORM,
                    url=url_key,
                    source=url_value,
                    album=album_orm,
                )
                # album_external_url_orm: AlbumExternalUrlORM = AlbumExternalUrlORM(
                # url=url_key,
                # source=url_value,
                # album=album_orm,
                # )
                # session.add(album_external_url_orm)
                album_external_urls_coll.append(album_external_url_orm)

            # Album Image
            album_images_coll = []
            for image in album_item.images:
                image: Image = image

                album_image_orm: AlbumImageORM = AlbumImageORM(
                    url=image.url,
                    width=image.width,
                    height=image.height,
                    album=album_orm,
                    album_id=album_orm.id,
                )
                print("***************\nalbum_image_orm is BELOW:")
                print(album_image_orm)
                print("***************\n")

                album_image_orm: AlbumImageORM = get_or_create(
                    session,
                    AlbumImageORM,
                    url=image.url,
                    width=image.width,
                    height=image.height,
                    album=album_orm,
                    album_id=album_orm.id,
                )
                # album_image_orm: AlbumImageORM = AlbumImageORM(
                #     url=image.url,
                #     width=image.width,
                #     height=image.height,
                #     album=album_orm,
                # )
                # session.add(album_image_orm)
                album_images_coll.append(album_image_orm)

            track_record: TrackRecordORM = get_or_create(
                session,
                TrackRecordORM,
                track=track_orm,
                type=track_item.type,
                played_at=activity.played_at,
            )
            # track_record: TrackRecordORM = TrackRecordORM(
            #     track=track_orm, type=track_item.type, played_at=activity.played_at
            # )

            # session.add(track_record)
            # session.add(track_orm)
            # session.add(album_orm)
            session.commit()
