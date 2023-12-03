from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from settings.config import ConfigExchangeApi


engine = create_engine(ConfigExchangeApi.DB_URL)

Session = sessionmaker(bind=engine)


def get_session():
    with Session() as session:
        yield session
