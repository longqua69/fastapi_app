"""Predefined exceptions for the routers."""

# pylint: disable=dangerous-default-value

from fastapi import HTTPException, status


class CredentialsException(HTTPException):
    """Exception raised for errors in the credentials."""

    def __init__(
        self,
        detail: str = "Could not validate credentials",
        headers: dict[str, str] = {"WWW-Authenticate": "Bearer"},
    ):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED, detail=detail, headers=headers
        )
