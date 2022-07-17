from sqlalchemy import Column, Integer

from sqlalchemy.orm import relationship
from .base import Base


class Event(Base):
    event_id = Column(Integer, nullable=False)
    score_index = Column(Integer, nullable=False)
    score1 = Column(Integer, nullable=False)
    score2 = Column(Integer, nullable=False)

