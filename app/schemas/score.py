from pydantic import BaseModel


class Score(BaseModel):
    score_index: int
    score1: int
    score2: int

    class Config:
        orm_mode = True
