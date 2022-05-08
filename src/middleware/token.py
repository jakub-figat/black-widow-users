from typing import Callable

from chalice.app import Request, Response

from app import app
from src.services import token_service


@app.middleware("http")
def authenticate_user(event: Request, get_response: Callable[[Request], Response]) -> Response:
    user = None
    if (auth_header := event.headers.get("Authorization")) is not None:
        user = token_service.authenticate_user_from_header(header=auth_header)

    event.user = user

    return get_response(event)
