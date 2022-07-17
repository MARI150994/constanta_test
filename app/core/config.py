import os
from pydantic import BaseSettings


class Settings(BaseSettings):
    SQLALCHEMY_PG_CONN_URI: str = os.getenv('DB_URL') or \
                                  'postgresql+asyncpg://user:password@localhost:5432/constanta'

settings = Settings()
