from sqlalchemy import (
    Column,
    Integer,
)
from sqlalchemy.orm import declared_attr
from sqlalchemy.ext.declarative import declarative_base


class Base:

    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    id = Column(Integer, primary_key=True)


Base = declarative_base(cls=Base)
