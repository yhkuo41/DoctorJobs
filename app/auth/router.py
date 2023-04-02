from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from pymongo.database import Database

from app.auth.jwt import create_access_token
from app.db import database
from app.user import service, hashing

auth_router = APIRouter(tags=['Auth'])


@auth_router.post('/login')
def login(request: OAuth2PasswordRequestForm = Depends(), db: Database = Depends(database.get_db)):
    """Notes: the username in OAuth2 Form is user's account"""
    user = service.get_user_by_account(request.username, db.user)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Invalid Credentials')

    if not hashing.verify_password(request.password, user.password.get_secret_value()):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Invalid Password')

    # Generate a JWT Token
    access_token = create_access_token(data={"sub": user.user_id})

    return {"access_token": access_token, "token_type": "bearer"}
