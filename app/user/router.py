from typing import Optional

from fastapi import APIRouter, status, HTTPException, Depends

from app.auth.jwt import get_current_user
from app.db.db import user_col
from app.user import schema, service
from app.user.schema import UserCreateResponse, User

user = APIRouter(tags=["User"], prefix="/user")


@user.post('/', status_code=status.HTTP_201_CREATED)
async def create_user_registration(request: schema.UserBase) -> UserCreateResponse:
    # TODO transaction if necessary
    exist = await service.verify_exist(request, user_col)
    if exist:
        raise HTTPException(
            status_code=400,
            detail="The user with this email or account already exists in the system.",
        )
    user_id = await service.new_user_register(request, user_col)
    return UserCreateResponse(id=user_id)


@user.get('/{user_id}')
async def get_user_by_user_id(user_id: str, current_user: User = Depends(get_current_user)) -> Optional[User]:
    u = await service.get_user_by_user_id(user_id, user_col)
    if u is None:
        raise HTTPException(status_code=404, detail=f"User not found")
    return u
