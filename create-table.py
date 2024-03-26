from sqlalchemy import create_engine

# from model import Base
from models.models import Base

db_url = "postgresql://postgres:example@localhost:8032/postgres"
engine = create_engine(db_url, echo=True)

print(engine)
print(Base.metadata.tables.values())
# Base.metadata

Base.metadata.drop_all(engine)

Base.metadata.create_all(engine)
