from typing import List, Optional

from fastapi import APIRouter, Query, HTTPException
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app import crud
from app.api.deps import get_db
from app.schemas import Score


router = APIRouter()


@router.get('/events')
async def read_events(
        db: AsyncSession = Depends(get_db)
):
    events_list = await crud.read_events(db)
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
