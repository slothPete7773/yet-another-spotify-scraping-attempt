from sqlalchemy import create_engine

from app.models.schema.models_orm import Base

from configparser import ConfigParser

config = ConfigParser()
config.read("env.conf")

import logging
from datetime import datetime

logging.basicConfig(
    filename=f"log/create-table-{datetime.now().strftime('%Y-%m-%d')}.log",
    filemode="a",
    level=logging.INFO,
    format="%(asctime)s - %(message)s",
)


ENV = "postgresql_dev"
USERNAME = config.get(ENV, "username")
PASSWORD = config.get(ENV, "password")
HOST = config.get(ENV, "host")
PORT = config.get(ENV, "port")
DEFAULT_DATABASE = config.get(ENV, "default_database")
pg_uri = f"postgresql://{USERNAME}:{PASSWORD}@{HOST}:{PORT}/{DEFAULT_DATABASE}"

logging.info(f"CONNECTED TO Postgresql WITH HOST: {HOST}.")
engine = create_engine(pg_uri, echo=True)

print(engine)
print(Base.metadata.tables.values())
# Base.metadata
logging.info("INITIATE DROP ALL TABLES.")
Base.metadata.drop_all(engine)
logging.info("SUCCESSFULLY DROPPED ALL TABLES.")

logging.info("INITIATE CREATE ALL TABLES.")
Base.metadata.create_all(engine)
logging.info("SUCCESSFULLY CREATED ALL TABLES.")
