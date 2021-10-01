from sqlalchemy import (
    Table,
    MetaData,
    Column,
    Integer,
    Boolean,
)
from sqlalchemy.engine import create_engine
from sqlalchemy.orm import mapper

from domain.model import UserCoins
import config

metadata = MetaData()

user_coins = Table(
    "user_coins",
    metadata,
    Column("user_id", Integer, primary_key=True, autoincrement=False),
    Column("coins", Integer),
)

def start_mappers():
    mapper(UserCoins, user_coins)


def create_tables():
    engine = create_engine(config.get_sqlite_uri())
    metadata.create_all(engine)
