import os
from datetime import datetime, timedelta, timezone
# import jwt
from jose import jwt
from fastapi import Depends, Header
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.base import get_db
from app.utils.error_handler import ErrorHandler
from app.controllers.user import UserController
from fastapi.security import HTTPBearer  # TODO Bearer

SECRET_KEY = os.environ.get("SECRET_KEY")
ALGORITHM = os.environ.get("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(
    os.environ.get("ACCESS_TOKEN_EXPIRE_MINUTES"))


def token_generator(user_id: int, scope: str):
    to_encode_data = {
        "user_id": user_id,
        "created_at": str(datetime.now())
    }

    # set expiration time for the token
    expire = datetime.now(timezone.utc) + \
        timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode_data.update({"exp": expire})

    return jwt.encode(to_encode_data, SECRET_KEY, ALGORITHM)


def token_decoder(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except jwt.ExpiredSignatureError:
        raise ErrorHandler.user_unauthorized(message="Auth token is expired.")
    except:
        raise ErrorHandler.user_unauthorized(
            message="Auth token is not valid.")

    return {
        "user_id": payload["user_id"],
    }


# dependency
async def get_token_info(auth_token: str = Header(...), db: AsyncSession = Depends(get_db)):
    if not auth_token:
        raise ErrorHandler.user_unauthorized(
            message="Auth token does not exist.")

    try:
        token_prefix, token_value = auth_token.split(" ")
    except Exception:
        raise ErrorHandler.user_unauthorized(
            message="Invalid authentication scheme for auth token (Use Bearer)")

    token_info = token_decoder(token_value)

    user_controller = UserController(db)
    user = await user_controller.get_by_id(id=token_info["user_id"])
    return {
        "user": user
    }
