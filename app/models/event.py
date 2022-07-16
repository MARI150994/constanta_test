from sqlalchemy import (Column,
                        Integer,
                        String,
                        JSON)

from .base import Base


class Event(Base):
    event_id = Column(Integer, nullable=False)
    scores = Column(JSON, nullable=False)
