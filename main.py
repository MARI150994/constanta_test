import json

import uvicorn
from fastapi import FastAPI

from app.api.endpoints import router
from app.crud import create_events
from app.models import Base
from app.models.db import database, async_session, engine

app = FastAPI()
app.include_router(router)


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


async def fill_db():
    res = []
    with open('input', 'r') as f:
        for _ in range(1001):
            messages = json.loads(f.readline())
            for message in messages:
                if message.get('class') != 'Fon.Notification.EventResultNotification':
                    continue
                # get event id
                event_id = message.get('object').get('eventResultId')

                # get list of scores
                scores = message.get('object').get('eventResultInstance').get('object').get('scores')

                # delete empty score list
                if scores == []:
                    continue

                for object in scores:
                    # get event from object
                    if object.get('class') != "Fon.Ora.ScoreBody":
                        continue
                    event = object.get('object')
                    event.pop('flags')

                    # give dict like {'scoreIndex': 0, 'score1': 0, 'score2':0}
                    async with async_session() as session:
                        await create_events(
                            db=session,
                            event_id=int(event_id),
                            score_index=event.get('scoreIndex'),
                            score1=event.get('score1'),
                            score2=event.get('score2'),
                        )


if __name__ == '__main__':
    uvicorn.run('main:app', host='0.0.0.0', port=8000, reload=True)
