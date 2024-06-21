from pydantic import EmailStr
from sqlmodel import Field, Relationship, SQLModel


# User
class UserBase(SQLModel):
    username: str = Field(unique=True, index=True)
    email: EmailStr = Field(unique=True, index=True, max_length=255)
    is_active: bool = True
    is_superuser: bool = False
    full_name: str | None = Field(default=None, max_length=255)


class UserCreate(UserBase):
    password: str = Field(min_length=8, max_length=40)


class User(UserBase, table=True):
    id: int = Field(primary_key=True)
    hashed_password: str
    items: list['Item'] = Relationship(back_populates='owner')


# Item
class ItemBase(SQLModel):
    title: str = Field(min_length=1, max_length=255)
    description: str | None = Field(default=None, max_length=255)


class ItemCreate(ItemBase):
    pass


class Item(ItemBase, table=True):
    id: int = Field(primary_key=True)
    owner_id: int = Field(foreign_key='user.id')
    owner: User = Relationship(back_populates='items')
