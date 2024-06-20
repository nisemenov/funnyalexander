from typing import Annotated
from fastapi import APIRouter, Depends

from backend.app.models import User
from api.deps import TokenDep

router = APIRouter()

def fake_decode_token(token):
    return User(
        username=token + "fakedecoded", email="john@example.com", full_name="John Doe"
    )


async def get_current_user(token: TokenDep):
    user = fake_decode_token(token)
    return user


@router.add_api_route('/login/access-token')
async def read_users_me(current_user: Annotated[User, Depends(get_current_user)]):
    return current_user
