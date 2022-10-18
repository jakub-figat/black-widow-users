from fastapi import Depends
from jwt import InvalidTokenError

from src.data_access.exceptions import DoesNotExist
from src.models.user import User
from src.routes.token import oauth2_scheme
from src.services import token_service, user_dynamodb_data_access
from src.services.token import TokenServiceException


def get_request_user(token: str = Depends(oauth2_scheme)) -> User:
    try:
        decoded_token = token_service.decode_token(token=token)
        user_key = f"user#{decoded_token['sub']}"
        user = user_dynamodb_data_access.get(pk=user_key, sk=user_key)
        if user is None:
            raise DoesNotExist(f"User with email {decoded_token['sub']} does not exist")

        return user

    except InvalidTokenError as exc:
        raise TokenServiceException("Could not authenticate user") from exc
