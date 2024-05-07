import json
from datetime import datetime
import uuid
import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.exc import NoResultFound

from models.models_orm import *
from models.models import *

from utils.database import Database

import logging
from datetime import datetime

logging.basicConfig(
    filename=f"log/insertion-{datetime.now().strftime('%Y-%m-%d')}.log",
    filemode="a",
    level=logging.INFO,
    format="%(asctime)s - %(message)s",
)

from configparser import ConfigParser

config = ConfigParser()
config.read("env.conf")


ENV = "postgresql_dev"
USERNAME = config.get(ENV, "username")
PASSWORD = config.get(ENV, "password")
HOST = config.get(ENV, "host")
PORT = config.get(ENV, "port")
DEFAULT_DATABASE = config.get(ENV, "default_database")
pg_uri = f"postgresql://{USERNAME}:{PASSWORD}@{HOST}:{PORT}/{DEFAULT_DATABASE}"

engine = create_engine(pg_uri, echo=False)
Session = sessionmaker(bind=engine, autoflush=False)


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


def map_with_pydantic(wrapper, objects):
    return [wrapper(**item) for item in objects]


with Session() as session:
    open_json_file = Database.open_json_file
    get_or_create = Database.get_or_create
    get_uuid4_str = Database.get_uuid4_str
    filepaths = get_all_filenames()
    for filepath in filepaths:
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
                release_date_precision=album_item.release_date_precision,
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
