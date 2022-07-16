from pydantic import BaseSettings


class Settings(BaseSettings):
    SQLALCHEMY_PG_CONN_URI: str = \
        'postgresql+asyncpg://user:password@localhost:5432/constanta'

settings = Settings()
