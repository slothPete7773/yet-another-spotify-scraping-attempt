from sqlalchemy import create_engine

from models.models_orm import Base

from configparser import ConfigParser

config = ConfigParser()
config.read("env.conf")

db_url = "postgresql://postgres:example@localhost:8032/postgres"
engine = create_engine(db_url, echo=True)

USERNAME = config.get("postgresql", "username")
PASSWORD = config.get("postgresql", "password")
HOST = config.get("postgresql", "host")
PORT = config.get("postgresql", "port")
DEFAULT_DATABASE = config.get("postgresql", "default_database")
pg_uri = f"postgresql://{USERNAME}:{PASSWORD}@{HOST}:{PORT}/{DEFAULT_DATABASE}"

logging.info(f"CONNECTED TO Postgresql WITH HOST: {HOST}.")
engine = create_engine(pg_uri, echo=True)

print(engine)
print(Base.metadata.tables.values())
# Base.metadata

Base.metadata.drop_all(engine)

Base.metadata.create_all(engine)
