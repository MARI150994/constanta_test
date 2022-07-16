import json
import logging

import uvicorn
from fastapi import FastAPI, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_db
from app.api.endpoints import router
from app.crud import create_events
from app.models import Base
from app.models.db import database, async_session, engine


app = FastAPI()
app.include_router(router)

# TODO drop all on shutdown

@app.on_event('startup')
async def startup():
    print('Check db connection...')
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    await database.connect()
    print('Conenction ok')
    print('Fill db, wait a minute please...')
    await fill_db()
    print('Finish fill db')

# TODO shutdown
#
# @app.on_event('shutdown')
# async def shutdown():
#     async with engine.begin() as conn:
#         print('Clear db')
#         async with async_session() as session:
#             await delete_events
#         print('Finish clear db')


async def fill_db():
    res = []
    with open('input', 'r') as f:
        for _ in range(50):
            d = json.loads(f.readline())
            if d[0].get('class') != 'Fon.Notification.EventResultNotification':
                continue
            # get event id
            event_id = d[0].get('object').get('eventResultId')
            # get list of scores
            score_events = d[0].get('object').get('eventResultInstance')\
                .get('object').get('scores')
            # delete empty score list
            if score_events == []:
                continue
            to_db_scores = []
            for event in score_events:
                e = event.get('object')
                e.pop('flags')
                to_db_scores.append(e)
            async with async_session() as session:
                await create_events(db=session,
                                   event_id=int(event_id),
                                   scores=to_db_scores)


if __name__ == '__main__':
    uvicorn.run('main:app', host='0.0.0.0', port=8000, reload=True)
