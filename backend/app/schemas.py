from pydantic import BaseModel, EmailStr

# User
class UserBase(BaseModel):
    username: str
    email: EmailStr
    is_active: bool = True
    is_superuser: bool = False
    full_name: str | None = None


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    hashed_password: str
    items: list['Item'] = []

    class Config:
        orm_mode = True


# Item
class ItemBase(BaseModel):
    title: str
    description: str | None = None


class ItemCreate(ItemBase):
    pass


class Item(ItemBase, table=True):
    id: int
    owner_id: int
    
    class Config:
        orm_mode = True
