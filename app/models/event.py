from sqlalchemy import Column, Integer

from sqlalchemy.orm import relationship
from .base import Base


class Event(Base):
    event_id = Column(Integer, nullable=False)
    scores = relationship('Score', back_populates='event')

