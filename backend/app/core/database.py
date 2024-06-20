from dotenv import load_dotenv
import os
from pydantic import PostgresDsn
from pydantic_core import MultiHostUrl
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# from app.models import User, Item

load_dotenv()

# SQLALCHEMY_DATABASE_URL = f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_SERVER}:{DB_PORT}/{DB_NAME}'

def SQLALCHEMY_DATABASE_URI() -> PostgresDsn:
    return MultiHostUrl.build(
        scheme='postgresql+psycopg2',
        username=os.getenv('POSTGRES_USER'),
        password=os.getenv('POSTGRES_PASSWORD'),
        host=os.getenv('POSTGRES_SERVER'),
        port=5444,
        path=os.getenv('POSTGRES_DB')
    )

engine = create_engine(str(SQLALCHEMY_DATABASE_URI()))
# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
