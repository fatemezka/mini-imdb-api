import logging
from datetime import datetime
from fastapi import status, HTTPException


class CustomException(HTTPException):
    def __init__(self, status_code: int, detail: str):
        self.status_code = status_code
        self.detail = detail


class ErrorHandler:
    @staticmethod
    def not_found(item: str):
        raise CustomException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"{item} Not Found"
        )

    @staticmethod
    def user_unauthorized(message: str):
        raise CustomException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=message
        )

    @staticmethod
    def access_denied(item: str):
        raise CustomException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"You do not have access to this {item}"
        )

    @staticmethod
    def blocked_ip():
        raise CustomException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Your IP is blocked"
        )

    @staticmethod
    def bad_request(custom_message):
        raise CustomException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=custom_message)

    @staticmethod
    def too_many_request():
        raise CustomException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS, detail="Too many request")
