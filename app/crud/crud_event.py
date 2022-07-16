from typing import Union, List, Dict

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import text

from app import models


async def create_events(
        db: AsyncSession,
        event_id: int,
        scores: Union[List, Dict]
) -> None:
    db_event = models.Event(
        event_id=event_id,
        scores=scores
    )
    db.add(db_event)
    await db.commit()


async def read_events(
        db: AsyncSession,
        skip: int,
        limit: int,
):
    # TODO select *
    # from event
    # where id in
    #     (select max(id) id
    #     from event
    #     group by event_id
    #     order by max(id) desc);
    outer_query = select(models.Event).where()
    q = await db.execute(text(outer_query))
    return q.scalars().all()


async def get_event(
        db: AsyncSession,
        event_id: int
):
    query = select(models.Event).filter(models.Event.event_id==event_id)
    q = await db.execute(query)
    return q.scalars().all()