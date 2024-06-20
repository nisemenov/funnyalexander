from dotenv import load_dotenv
import os
from pydantic import PostgresDsn
from pydantic_core import MultiHostUrl
from sqlalchemy import create_engine


load_dotenv()


def SQLALCHEMY_DATABASE_URI() -> PostgresDsn:
    POSTGRES_PORT: int = int(os.getenv('POSTGRES_PORT', '5432'))

    return MultiHostUrl.build(
        scheme='postgresql+psycopg',
        username=os.getenv('POSTGRES_USER'),
        password=os.getenv('POSTGRES_PASSWORD'),
        host=os.getenv('POSTGRES_SERVER'),
        port=POSTGRES_PORT,
        path=os.getenv('POSTGRES_DB')
    )

engine = create_engine(str(SQLALCHEMY_DATABASE_URI()))
