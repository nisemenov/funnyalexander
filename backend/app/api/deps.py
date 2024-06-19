from typing import Annotated, Generator
from sqlmodel import Session

from app.core.database import engine


def get_db() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session

SessionDep = Annotated[Session, get_db]
