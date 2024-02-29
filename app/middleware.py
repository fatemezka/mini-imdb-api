from fastapi import Request, Response, status
from datetime import datetime
from starlette.middleware.base import BaseHTTPMiddleware
from datetime import datetime
from app.utils.error_handler import CustomException, ErrorHandler
from app.authentication import token_encoder
from app.redis import get_redis_value, increase_redis_request_ip, get_allowed_ip_list
from app.models import User
from app.database import SessionLocal
from sqlalchemy import select
from fastapi.responses import JSONResponse
import logging


class CustomMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        try:
            # check ip
            await self.check_allowed_ip(request)

            # check request count per minute
            if request.method == "POST" and request.url.path == "/user/token":
                await self.check_request_attempts(request)

            # validate token from redis
            await self.validate_token(request)

            # log request
            self.log_request(request)

            # Continue processing the request
            response: Response = await call_next(request)
            return response

        except CustomException as e:
            return JSONResponse(status_code=e.status_code, content={"message": e.detail})
        except Exception as e:
            logging.error(f"An error occurred at {datetime.now()}: {e}")
            return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                content={"message": "Something went wrong in our server!"})

    def log_request(self, request: Request):
        if request.client:
            client_ip = request.client.host
        else:
            client_ip = "N/A"  # for unit-testing

        current_date = str(datetime.now())
        request_data = f"Date: {current_date}, Request Method: {request.method}, Client Ip: {client_ip} {request.headers}\n"
        with open("request_logger.log", 'a') as log_file:
            log_file.write(request_data)

    async def check_allowed_ip(self, request: Request):
        allowed_ip_list = await get_allowed_ip_list()

        if request.client:
            client_ip = request.client.host
        else:
            client_ip = "N/A"  # for unit-testing

        if client_ip != "N/A" and client_ip not in allowed_ip_list:
            raise ErrorHandler.blocked_ip()

    async def validate_token(self, request: Request):
        if "auth-token" not in request.headers:
            return

        try:
            bearer, token = request.headers["auth-token"].split(" ")
            encoded_token = token_encoder(token=token)
            user_id = encoded_token["user_id"]
        except:
            raise ErrorHandler.user_unauthorized(
                message="Auth token is not valid.")

        db = SessionLocal()
        current_user = (await db.execute(select(User).where(User.id == user_id))).scalar_one_or_none()

        existing_redis_token = await get_redis_value(key=current_user.email)
        if not existing_redis_token:
            raise ErrorHandler.user_unauthorized(
                message="Your token is expired. Please try to login again.")

    async def check_request_attempts(self, request: Request):
        if not request.client:
            return
        client_ip = request.client.host
        await increase_redis_request_ip(client_ip)
