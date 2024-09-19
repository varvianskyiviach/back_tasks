from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from auth.schemas import TokenSchema
from config import settings
from users import crud
from users.deps import SessionDep
from utils import security

router = APIRouter(prefix="/auth")


@router.post("/token")
def login_access_token(db: SessionDep, form_data: Annotated[OAuth2PasswordRequestForm, Depends()]) -> TokenSchema:
    user = crud.authenticate(db=db, email=form_data.username, password=form_data.password)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    elif not user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    access_token_expires = timedelta(settings.ACCESS_TOKEN_EXPIRE_MINUTES)

    return TokenSchema(access_token=security.create_access_token(user.id, expires_delta=access_token_expires))
