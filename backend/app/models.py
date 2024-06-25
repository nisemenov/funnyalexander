from pydantic import EmailStr
from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = 'users'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(30), unique=True)
    full_name: Mapped[str | None] = mapped_column(default=None)
    email: Mapped[str] = mapped_column(unique=True)
    is_active: Mapped[bool] = mapped_column(default=True)
    is_superuser: Mapped[bool] = mapped_column(default=False)
    hashed_password: Mapped[str]

    items: Mapped[list['Item']] = relationship(back_populates='owner')

    def __repr__(self) -> str:
        return (f'User(id={self.id!r}, username={self.username!r}, '
                f'fullname={self.full_name!r})')


class Item(Base):
    __tablename__ = 'items'

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(255))
    description: Mapped[str | None] = mapped_column(String(255), default=None)
    owner_id = mapped_column(ForeignKey('users.id'))

    owner: Mapped[User] = relationship(back_populates='items')

    def __repr__(self) -> str:
        return f'Item(id={self.id!r}, title={self.title})'
