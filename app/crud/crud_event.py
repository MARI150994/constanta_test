from typing import Union, List, Dict, Optional

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import func, and_

from app import models
from app.schemas import Score


async def create_events(
        db: AsyncSession,
        event_id: int,
        score_index: int,
        score1: int,
        score2: int
) -> None:
    # check if event with this score_index already exist
    event = select(models.Event) \
        .filter(and_(models.Event.event_id == event_id,
                     models.Event.score_index == score_index,
                     models.Event.score1 == score1,
                     models.Event.score2 == score2))
    q = await db.execute(event)
    event = q.scalars().first()
    # if this event already exist - do nothing
    if event:
        return

    # if event doesn't exist - create new
    db_event = models.Event(
        event_id=event_id,
        score_index=score_index,
        score1=score1,
        score2=score2
    )
    db.add(db_event)
    await db.commit()
    return


async def read_events(
        db: AsyncSession,
):
    # select distinct event_id
    events = select(models.Event.event_id).distinct(models.Event.event_id)
    events_list = {}
    q = await db.execute(events)
    for event_id in q.scalars().all():
        subq = select(func.max(models.Event.id).label('id')) \
            .filter(models.Event.event_id == event_id) \
            .group_by(models.Event.score_index)
        query = select(models.Event) \
            .filter(models.Event.id.in_(subq))
        q = await db.execute(query)
        scores = q.scalars().all()
        events_list[event_id] = [
            Score(**{'score_index': score.score_index,
                     'score1': score.score1,
                     'score2': score.score2}) for score in scores]
    return events_list


async def get_event(
        db: AsyncSession,
        event_id: int
):
    query = select(models.Event).filter(models.Event.event_id == event_id).order_by(models.Event.id)
    q = await db.execute(query)
    event_history = q.scalars().all()
    if not event_history:
        raise HTTPException(status_code=404, detail="Event with this event id doesn't exist")
    return event_history
