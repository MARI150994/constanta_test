from sqlalchemy import (Column,
                        Integer,
                        ForeignKey)
from sqlalchemy.orm import relationship
from .base import Base


class Score(Base):
    event_id = Column(Integer, ForeignKey('event.id'), nullable=False)
    score_index = Column(Integer, nullable=False)
    score1 = Column(Integer, nullable=False)
    score2 = Column(Integer, nullable=False)
    event = relationship('Event', back_populates='scores')
