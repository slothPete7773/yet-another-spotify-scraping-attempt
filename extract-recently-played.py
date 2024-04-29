import json
from datetime import datetime
import uuid
import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.exc import NoResultFound

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


from configparser import ConfigParser

config = ConfigParser()
config.read("env.conf")


filename = "test_file-original.json"

USERNAME = config.get("postgresql", "username")
PASSWORD = config.get("postgresql", "password")
HOST = config.get("postgresql", "host")
PORT = config.get("postgresql", "port")
DEFAULT_DATABASE = config.get("postgresql", "default_database")
pg_uri = f"postgresql://{USERNAME}:{PASSWORD}@{HOST}:{PORT}/{DEFAULT_DATABASE}"

engine = create_engine(pg_uri, echo=False)
Session = sessionmaker(bind=engine, autoflush=False)


def get_uuid4_str() -> str:
    return str(uuid.uuid4())


def get_or_create(session, model, **kwargs):
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
            mtext = f"model:{model}, args:{kwargs} => msg:{msg}"
            session.rollback()
            raise (msg)
        return instance

    instance = get_instance(session, model, **kwargs)
    if instance is None:
        instance = create_instance(session, model, **kwargs)

    return instance


def get_all_filenames() -> list[str]:
    LANDING_SOURCE_DIR = "landing"
    filenames = os.listdir(LANDING_SOURCE_DIR)

    return list(
        filter(
            lambda x: x[-5:] == ".json",
            [f"{LANDING_SOURCE_DIR}/{filename}" for filename in filenames],
        )
    )


def move_done_to_processed(src_path, dest_path):
    os.rename(src_path, dest_path)


def open_json_file(filepath):
    try:
        if os.path.isfile(filepath):
            with open(filepath) as file:
                return json.load(file)
        else:
            return None
    except FileNotFoundError as e:
        print(f"Error: Ensure file is existed.")
        return e


def map_with_pydantic(wrapper, objects):
    return [wrapper(**item) for item in objects]


with Session() as session:
    filepaths = get_all_filenames()
    for filepath in filepaths:
        print(f"Processing file: {filepath}")
        file_content = open_json_file(filepath)
        recorded_activities: list = file_content["items"]

        activities = [TrackRecord(**record) for record in recorded_activities]

        for activity in activities:
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
                artists_coll.append(artist_orm)

                track_feature_orm: TrackFeatureORM = get_or_create(
                    session,
                    TrackFeatureORM,
                    track=track_orm,
                    artist=artist_orm,
                )
                track_features_coll.append(track_feature_orm)

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
                album_external_urls_coll.append(album_external_url_orm)

            # Album Image
            album_images_coll = []
            for image in album_item.images:
                image: Image = image

                album_image_orm: AlbumImageORM = get_or_create(
                    session,
                    AlbumImageORM,
                    id=get_uuid4_str(),
                    url=image.url,
                    width=image.width,
                    height=image.height,
                    album_id=album_orm.id,
                    album=album_orm,
                )

            track_record: TrackRecordORM = get_or_create(
                session,
                TrackRecordORM,
                track=track_orm,
                type=track_item.type,
                played_at=activity.played_at,
            )
            session.commit()

        dest_path = os.path.join("processed", filepath.split("/")[-1])
        move_done_to_processed(filepath, dest_path)
