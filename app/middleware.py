from fastapi import Request, Response, status
from datetime import datetime
from starlette.middleware.base import BaseHTTPMiddleware
from datetime import datetime
from app.utils.error_handler import CustomException
from app.controllers.redis_pool import RedisPool
from fastapi.responses import JSONResponse
import logging


class CustomMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        try:
            # check request count per minute
            await self.check_request_attempts(request)

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

    async def check_request_attempts(self, request: Request):
        if not request.client:
            return  # for unit-testing
        client_ip = request.client.host
        redis_pool = RedisPool()
        await redis_pool.increase_request_attempts(client_ip)
