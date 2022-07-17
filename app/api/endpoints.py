from typing import List, Optional

from fastapi import APIRouter, Query, HTTPException
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app import crud
from app.api.deps import get_db
from app.schemas import Score, Event, ScoreE


router = APIRouter()

# TODO
#
# select *
# from score
# join event e on e.id = score.event_id
# where score.id in
#       (select max(id) id
#        from score
#        group by event_id, score_index
#        order by event_id)
# order by score.event_id, score.id desc


@router.get('/events/')
async def read_events(
        db: AsyncSession = Depends(get_db),
        skip: int = 0,
        limit: int = 1000
):
    events_list = await crud.read_events(db, skip, limit)
    print('EVENTS LIST FROM READ EVENTS ENDPOINT', events_list)
    return events_list


@router.get('/events/{event_id}', response_model=List[Score])
async def read_event_history(
        *,
        db: AsyncSession = Depends(get_db),
        event_id: int
):
    event_history = await crud.get_event(
        db=db,
        event_id=event_id
    )
    return event_history
