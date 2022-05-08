import datetime as dt
from typing import Any
from uuid import uuid4

import jwt

from src.enums import TokenType
from src.settings import settings


class TokenService:
    @classmethod
    def _create_token(cls, subject: str, token_type: TokenType) -> str:
        expire_times = {
            TokenType.ACCESS: settings.access_token_lifetime_in_minutes,
            TokenType.REFRESH: settings.refresh_token_lifetime_in_minutes,
        }

        now = dt.datetime.utcnow()
        expire_time = now + dt.timedelta(minutes=expire_times[token_type])
        token_payload = {"sub": subject, "jti": str(uuid4()), "iat": now.timestamp(), "exp": expire_time.timestamp()}

        return jwt.encode(payload=token_payload, key=settings.secret_key)

    @classmethod
    def create_token_pair(cls, subject: str) -> dict[str, str]:
        return {
            "access_token": cls._create_token(subject=subject, token_type=TokenType.ACCESS),
            "refresh_token": cls._create_token(subject=subject, token_type=TokenType.REFRESH),
        }

    @classmethod
    def decode_token(cls, token: str) -> dict[str, Any]:
        return jwt.decode(jwt=token, key=settings.secret_key)
