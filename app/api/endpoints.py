from typing import List, Optional

from fastapi import APIRouter, Query, HTTPException
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app import crud
from app.api.deps import get_db


router = APIRouter()


@router.get('/events/')
async def read_events(
        db: AsyncSession = Depends(get_db),
        skip: int = 0,
        limit: int = 1000
):
    events = await crud.read_events(db, skip, limit)
    print('events from endpoint', events)
    return events


@router.get('/events/{event_id}')
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
