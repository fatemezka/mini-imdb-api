from fastapi import APIRouter, Depends, Path, Body
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.base import get_db
from app.schemas import ICreateUserBody, ILoginUser, IUpdateUserBody
from app.utils.error_handler import ErrorHandler
from app.controllers.user import UserController
from app.dependencies.authentication import token_generator, get_token_info
from app.utils.password_operator import get_password_hash
from app.controllers.redis import RedisController
from datetime import datetime


router = APIRouter()


# register
@router.post("/register")
async def register_route(
        data: ICreateUserBody = Body(description="User data to register"),
        db: AsyncSession = Depends(get_db)
):
    user_controller = UserController(db)

    # check username
    await user_controller.check_username_not_exists(data.username)

    # check username characters
    user_controller.validate_username_characters(data.username)

    # check email
    await user_controller.check_email_not_exists(data.email)

    # check dob
    if (data.dob):
        data.dob = await user_controller.validate_dob(dob=data.dob)

    # validate password characters
    user_controller.validate_password_characters(data.password)

    # hash user's password
    hashed_password = get_password_hash(data.password)

    # create a new user
    user_items = {
        "username": data.username,
        "email": data.email,
        "hashedPassword": hashed_password,
        "fullname": data.fullname or None,
        "dob": data.dob or None,
        "gender": data.gender or None
    }
    user = await user_controller.create(user_items=user_items)
    await db.close()

    # generate jwt token
    user_token = token_generator(
        user_id=user.id, scope="user")  # or admin

    # store user token in redis
    await store_redis_token(user=user, token=user_token)

    return {
        "user": user,
        "token": user_token
    }


# login
@router.post("/token")
async def login_route(
        data: ILoginUser = Body(description="User data to login"),
        db: AsyncSession = Depends(get_db)
):
    user_controller = UserController(db)

    # check username
    await user_controller.check_username_exists(data.username)

    # verify password
    await user_controller.verify_password(data.username, data.password)

    await db.close()

    # generate jwt token
    user = await user_controller.get_by_username(data.username)
    token = token_generator(user_id=user.id, scope="user")  # or admin

    # store user token in redis
    await remove_redis_token(user=user)
    await store_redis_token(user=user, token=token)

    return {
        "user": user,
        "token": token
    }
