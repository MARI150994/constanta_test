import databases
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession

from app.core.config import settings

PG_CONN_URI = settings.SQLALCHEMY_PG_CONN_URI

engine = create_async_engine(PG_CONN_URI, echo=False)
async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)
database = databases.Database(PG_CONN_URI)
