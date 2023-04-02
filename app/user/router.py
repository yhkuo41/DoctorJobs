from typing import Optional

from fastapi import APIRouter, status, HTTPException, Depends
from pymongo.database import Database

from app.auth.jwt import CurrentUserDep
from app.db import database
from app.user import schema, service
from app.user.schema import UserCreateResponse, User

user_router = APIRouter(tags=["User"], prefix="/user")


@user_router.post('/', status_code=status.HTTP_201_CREATED)
async def create_user_registration(request: schema.UserBase,
                                   db: Database = Depends(database.get_db)) -> UserCreateResponse:
    # TODO transaction if necessary
    exist = await service.verify_exist(request, db.user)
    if exist:
        raise HTTPException(
            status_code=400,
            detail="The user with this email or account already exists in the system.",
        )
    user_id = await service.new_user_register(request, db.user)
    return UserCreateResponse(user_id=user_id)


@user_router.get('/me')
async def get_current_user(current_user: CurrentUserDep,
                           db: Database = Depends(database.get_db)) -> Optional[User]:
    user = await service.get_user_by_user_id(current_user.user_id, db.user)
    if user is None:
        raise HTTPException(status_code=404, detail=f"User not found")
    return user
