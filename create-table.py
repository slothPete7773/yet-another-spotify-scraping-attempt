from sqlalchemy import create_engine

from models.models_orm import Base

db_url = "postgresql://postgres:example@localhost:8032/postgres"
engine = create_engine(db_url, echo=True)

print(engine)
print(Base.metadata.tables.values())
# Base.metadata

Base.metadata.drop_all(engine)

Base.metadata.create_all(engine)
