import datetime as dt
from typing import Any, Optional
from uuid import uuid4

import jwt
from chalice import BadRequestError

from chalicelib.data_access.user import UserDynamoDBDataAccess
from chalicelib.enums import TokenType
from chalicelib.models.token import TokenPairOutput
from chalicelib.models.user import User, UserLoginInput
from chalicelib.settings import settings


class TokenService:
    def __init__(self, user_data_access: UserDynamoDBDataAccess) -> None:
        self._user_data_access = user_data_access

    @classmethod
    def _create_token(cls, subject: str, token_type: TokenType) -> str:
        expire_times = {
            TokenType.ACCESS: settings.access_token_lifetime_in_minutes,
            TokenType.REFRESH: settings.refresh_token_lifetime_in_minutes,
        }

        now = dt.datetime.utcnow()
        expire_time = now + dt.timedelta(minutes=expire_times[token_type])
        token_payload = {
            "sub": subject,
            "jti": str(uuid4()),
            "iat": now.timestamp(),
            "exp": expire_time.timestamp(),
            "type": token_type.value,
        }

        return jwt.encode(payload=token_payload, key=settings.secret_key)

    @classmethod
    def validate_token_payload(cls, payload: dict[str, Any], token_type: TokenType) -> None:
        if payload["type"] != token_type.value:
            raise BadRequestError("Invalid token type")

        if payload["exp"] <= dt.datetime.utcnow().timestamp():
            raise BadRequestError("Token has expired")

    @classmethod
    def parse_token_from_header(cls, header: str) -> str:
        try:
            prefix, token = header.split(" ", 1)
        except ValueError as error:
            raise BadRequestError("Invalid bearer token") from error

        if not token.strip():
            raise BadRequestError("Invalid bearer token")

        if prefix != "Bearer":
            raise BadRequestError("Invalid bearer token")

        return token

    @classmethod
    def create_token_pair(cls, subject: str) -> dict[str, str]:
        return {
            "access_token": cls._create_token(subject=subject, token_type=TokenType.ACCESS),
            "refresh_token": cls._create_token(subject=subject, token_type=TokenType.REFRESH),
        }

    @classmethod
    def decode_token(cls, token: str) -> dict[str, Any]:
        return jwt.decode(jwt=token, key=settings.secret_key, algorithms=["HS256"])

    def authenticate_user_from_header(self, header: str) -> User:
        token = self.parse_token_from_header(header=header)
        payload = self.decode_token(token=token)
        self.validate_token_payload(payload=payload, token_type=TokenType.ACCESS)

        user_key = f"user#{payload['sub']}"
        user: Optional[User] = self._user_data_access.get(pk=user_key, sk=user_key)

        if user is None:
            raise BadRequestError("Token credentials are invalid")

        return user

    def create_token_pair_by_login(self, login_input: UserLoginInput) -> TokenPairOutput:
        if not self._user_data_access.check_password(**login_input.dict()):
            raise BadRequestError("Given credentials are invalid")

        token_pair = self.create_token_pair(subject=login_input.email)
        self.save_user_refresh_token(refresh_token=token_pair["refresh_token"], user=User(email=login_input.email))

        return TokenPairOutput(**token_pair)

    def create_token_pair_by_refresh(self, refresh_token: str) -> TokenPairOutput:
        payload = self.decode_token(token=refresh_token)
        self.validate_token_payload(payload=payload, token_type=TokenType.REFRESH)

        user_key = f"user#{payload['sub']}"
        user: Optional[User] = self._user_data_access.get(pk=user_key, sk=user_key)

        if user is None:
            raise BadRequestError("Invalid refresh token")

        token_pair = self.create_token_pair(subject=user.email)
        self.save_user_refresh_token(refresh_token=token_pair["refresh_token"], user=user)

        return TokenPairOutput(**token_pair)

    def save_user_refresh_token(self, refresh_token: str, user: User) -> None:
        jti = self.decode_token(token=refresh_token)["jti"]
        self._user_data_access.add_refresh_token_jti(user=user, refresh_token_jti=jti)

    def revoke_user_refresh_tokens(self, user: User) -> None:
        self._user_data_access.delete_user_refresh_token_jtis(user=user)
