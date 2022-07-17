from typing import Union, List, Dict, Optional

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import text, func
from sqlalchemy.orm import Session

from app import models
from app.schemas import Score

#
# async def get_event_by_event_id(
#         db: AsyncSession,
#         event_id: int,
# ) -> models.Event:
#     query = select(models.Event).filter(models.Event.event_id==event_id)
#     q = await db.execute(query)
#     return q.scalars().first()


def get_event_by_event_id(
        db: AsyncSession,
        event_id: int,
) -> models.Event:
    query = select(models.Event).filter(models.Event.event_id==event_id).with_for_update()
    q = db.execute(query)
    return q.scalars().first()


def create_events(
        db: Session,
        event_id: int,
        score_index: int,
        score1: int,
        score2: int
) -> None:
    event_exist = get_event_by_event_id(db, event_id)
    if not event_exist:
        db_event = models.Event(
            event_id=event_id,
        )
        db.add(db_event)
        db.commit()
        db.refresh(db_event)
        # event = await db.flush(db_event)
        db_score = models.Score(
            event_id=db_event.id,
            score_index=score_index,
            score1=score1,
            score2=score2
        )
        db.add(db_score)
        db.commit()
    # if event_exist
    else:
        # check if score with this score_index already exist
        current_score = select(models.Score)\
            .join(models.Event)\
            .filter(models.Event.event_id == event_id)\
            .filter(models.Score.score_index == score_index)\
            .order_by(models.Score.id.desc())
        q = db.execute(current_score)
        score = q.scalars().first()
        # if not exist score with this scoreIndex - create score
        if not score:
            db_score = models.Score(
                event_id=event_exist.id,
                score_index=score_index,
                score1=score1,
                score2=score2
            )
            db.add(db_score)
            db.commit()
            return
        # if exist check if score1 or score2 was changed
        else:

            if score.score1 != score1 or score.score2 != score2:
                db_score = models.Score(
                    event_id=event_exist.id,
                    score_index=score_index,
                    score1=score1,
                    score2=score2
                )
                db.add(db_score)
                db.commit()



#
# async def create_events(
#         db: AsyncSession,
#         event_id: int,
#         score_index: int,
#         score1: int,
#         score2: int
# ) -> None:
#     event_exist = await get_event_by_event_id(db, event_id)
#     if not event_exist:
#         db_event = models.Event(
#             event_id=event_id,
#         )
#         db.add(db_event)
#         await db.commit()
#         await db.refresh(db_event)
#         # event = await db.flush(db_event)
#         db_score = models.Score(
#             event_id=db_event.id,
#             score_index=score_index,
#             score1=score1,
#             score2=score2
#         )
#         db.add(db_score)
#         await db.commit()
#     else:
#         # check if score with this score_index already exist
#         current_score = select(models.Score).with_for_update().filter(event_id == event_id)\
#             .filter(models.Score.score_index == score_index)\
#             .order_by(models.Score.id.desc())
#         q = await db.execute(current_score)
#         score = q.scalars().first()
#         # if not exist score with this scoreIndex - create score
#         if not score:
#             print('score not exist, event_id, score_index, score1, score2', event_id, score_index, score1, score2)
#             db_score = models.Score(
#                 event_id=event_exist.id,
#                 score_index=score_index,
#                 score1=score1,
#                 score2=score2
#             )
#             db.add(db_score)
#             await db.commit()
#             return
#         # if exist check if score1 or score2 was changed
#         else:
#             print('score EXIST, event_id, score_index, score1, score2', event_id, score_index, score1, score2)
#             if score.score1 != score1 or score.score2 != score2:
#                 db_score = models.Score(
#                     event_id=event_exist.id,
#                     score_index=score_index,
#                     score1=score1,
#                     score2=score2
#                 )
#                 db.add(db_score)
#                 await db.commit()


async def read_events(
        db: AsyncSession,
        skip: int,
        limit: int,
):
    events = select(models.Event).order_by(models.Event.id)
    events_list = {}
    q = await db.execute(events)
    for event in q.scalars().all():
        # print('event', event.id)
        # for event in await db.execute(events):
        # event_id = event[0].event_id
        # event_pk = event[0].id
        print('event pk, event_id', event.event_id, event.id)
        subq = select(func.max(models.Score.id).label('id'))\
            .filter(models.Score.event_id == event.id)\
            .group_by(models.Score.score_index).subquery()
        query = select(models.Score)\
            .filter(models.Score.id.in_((subq)))
        q = await db.execute(query)
        scores = q.scalars().all()
        events_list[event.event_id] = scores
    return events_list

    #
    #
    # subq = select(func.max(models.Score.id).label('id'))\
    #     .group_by(models.Score.event_id, models.Score.score_index).subquery()
    # query = select(models.Score).filter(models.Score.id.in_((subq))).order_by(models.Score.event_id, models.Score.id)
    # q = await db.execute(query)
    # return q.scalars().all()


async def get_event(
        db: AsyncSession,
        event_id: int
):
    query = select(models.Score) \
        .join(models.Event) \
        .filter(models.Event.event_id == event_id)\
        .order_by(models.Score.id)
    q = await db.execute(query)
    return q.scalars().all()
