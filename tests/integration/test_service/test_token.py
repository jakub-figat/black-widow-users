import datetime as dt
from typing import Any

import jwt
import pytest
from chalice import BadRequestError

from src.data_access.user import UserDynamoDBDataAccess
from src.enums import TokenType
from src.models.user import User, UserLoginInput
from src.services import TokenService
from src.settings import settings


@pytest.fixture
def token_service(user_dynamodb_data_access: UserDynamoDBDataAccess) -> TokenService:
    return TokenService(user_data_access=user_dynamodb_data_access)


@pytest.fixture
def token_service_with_user_inserted(user_dynamodb_data_access: UserDynamoDBDataAccess) -> TokenService:
    user_dynamodb_data_access.create_user_with_password(email="testing@op.pl", password="test_password123")
    return TokenService(user_data_access=user_dynamodb_data_access)


@pytest.fixture
def token_service_with_refresh_token_inserted(user_dynamodb_data_access: UserDynamoDBDataAccess) -> TokenService:
    user_dynamodb_data_access.create(model=User(email="testing@op.pl", refresh_token_jtis=["abc"]))
    return TokenService(user_data_access=user_dynamodb_data_access)


def test_token_service_create_token_and_decode(token_service: TokenService) -> None:
    token = token_service._create_token(subject="username", token_type=TokenType.ACCESS)
    payload = token_service.decode_token(token=token)

    assert payload["type"] == TokenType.ACCESS.value
    assert payload["iat"] < dt.datetime.utcnow().timestamp()
    assert payload["exp"] > (dt.datetime.utcnow().timestamp() + settings.access_token_lifetime_in_minutes * 60 - 360)


@pytest.mark.parametrize(
    "payload,token_type",
    [
        ({"exp": dt.datetime.now().timestamp() - 30, "type": TokenType.ACCESS.value}, TokenType.ACCESS),
        (
            {
                "exp": dt.datetime.now().timestamp() + settings.refresh_token_lifetime_in_minutes * 36000,
                "type": TokenType.ACCESS.value,
            },
            TokenType.REFRESH,
        ),
    ],
)
def test_token_service_raises_bad_request_error_when_invalid_token_is_passed(
    payload: dict[str, Any], token_type: TokenType, token_service: TokenService
) -> None:
    with pytest.raises(BadRequestError):
        token_service.validate_token_payload(payload=payload, token_type=token_type)


def test_token_service_can_parse_token_from_header(token_service: TokenService) -> None:
    assert token_service.parse_token_from_header(header="Bearer abcdefg") == "abcdefg"


@pytest.mark.parametrize("header", ["Beare asdasdasd", "Bearer ", "Bearer     ", "abc", "bearer", "Bearer", ""])
def test_token_service_raises_bad_request_error_on_parsing_header_when_header_is_invalid(
    header: str, token_service: TokenService
) -> None:
    with pytest.raises(BadRequestError):
        token_service.parse_token_from_header(header=header)


def test_token_service_can_create_token_pair(token_service: TokenService) -> None:
    token_pair = token_service.create_token_pair(subject="somesubject")
    decoded_access = token_service.decode_token(token=token_pair["access_token"])
    decoded_refresh = token_service.decode_token(token=token_pair["refresh_token"])

    assert decoded_access["type"] == TokenType.ACCESS.value
    assert decoded_refresh["type"] == TokenType.REFRESH.value
    assert decoded_access["sub"] == decoded_refresh["sub"] == "somesubject"


def test_token_service_can_create_token_pair_by_login(token_service_with_user_inserted: TokenService) -> None:
    token_pair = token_service_with_user_inserted.create_token_pair_by_login(
        login_input=UserLoginInput(email="testing@op.pl", password="test_password123")
    )
    access_token_payload = token_service_with_user_inserted.decode_token(token=token_pair.access_token)

    assert access_token_payload["sub"] == "testing@op.pl"


def test_token_service_can_create_token_pair_by_refresh(
    token_service_with_refresh_token_inserted: TokenService,
) -> None:
    refresh_token = jwt.encode(
        payload={
            "jti": "abc",
            "sub": "testing@op.pl",
            "exp": dt.datetime.now().timestamp() + settings.refresh_token_lifetime_in_minutes * 60,
            "type": TokenType.REFRESH.value,
        },
        key=settings.secret_key,
        algorithm="HS256",
    )

    token_pair = token_service_with_refresh_token_inserted.create_token_pair_by_refresh(refresh_token=refresh_token)
    access_token_payload = token_service_with_refresh_token_inserted.decode_token(token=token_pair.access_token)

    assert access_token_payload["sub"] == "testing@op.pl"
