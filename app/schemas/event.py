from typing import List

from pydantic import BaseModel


class ScoreE(BaseModel):
    id: int
    event_id: int
    score_index: int
    score1: int
    score2: int

    class Config:
        orm_mode = True


class Event(BaseModel):
    event_id: int
    # scores: List[ScoreE]

    class Config:
        orm_mode = True
