import datetime as dt
import json

import jwt
import pytest
from chalice.test import Client
from mypy_boto3_dynamodb.service_resource import Table

from src.enums import TokenType
from src.models.user import User, UserRegisterInput
from src.services import token_service, user_service
from src.settings import settings


@pytest.fixture
def registered_user(dynamodb_testcase_table: Table) -> User:
    return user_service.register_user(
        input_model=UserRegisterInput(
            email="janusz123@op.pl", password="password12345", password_again="password12345"
        )
    )


@pytest.fixture
def refresh_token(registered_user: User) -> str:
    refresh_token = jwt.encode(
        payload={
            "sub": registered_user.email,
            "jti": "abc",
            "iat": dt.datetime.utcnow().timestamp(),
            "exp": dt.datetime.utcnow().timestamp() + settings.refresh_token_lifetime_in_minutes * 60,
            "type": TokenType.REFRESH.value,
        },
        key=settings.secret_key,
        algorithm="HS256",
    )

    token_service.save_user_refresh_token(refresh_token=refresh_token, user=registered_user)
    return refresh_token


@pytest.fixture
def access_token(registered_user: User) -> str:
    return token_service._create_token(subject=registered_user.email, token_type=TokenType.ACCESS)


def test_user_can_get_token_pair(test_client: Client, registered_user: User) -> None:
    request_body = {"email": "janusz123@op.pl", "password": "password12345"}

    response = test_client.http.post(
        "/tokens", body=json.dumps(request_body), headers={"Content-Type": "application/json"}
    )
    response_data = response.json_body

    assert response.status_code == 200
    assert "access_token" in response_data
    assert "refresh_token" in response_data


def test_user_cannot_get_token_pair_with_invalid_credentials(test_client: Client, registered_user: User) -> None:
    requests_body = {"email": "janusz123@op.pl", "password": "invaaaaalid"}
    response = test_client.http.post(
        "/tokens", body=json.dumps(requests_body), headers={"Content-Type": "application/json"}
    )

    response_data = response.json_body

    assert response.status_code == 400
    assert response_data == {"Code": "BadRequestError", "Message": "Given credentials are invalid"}


def test_user_can_get_token_pair_by_refresh(test_client: Client, registered_user: User, refresh_token: str) -> None:
    headers = {"Authorization": f"Bearer {refresh_token}"}
    response = test_client.http.post("/tokens/refresh", headers=headers)

    response_data = response.json_body

    assert response.status_code == 200
    assert "access_token" in response_data
    assert "refresh_token" in response_data


def test_user_cannot_get_token_pair_by_refresh_with_empty_authorization_header(
    test_client: Client, registered_user: User
) -> None:
    response = test_client.http.post("/tokens/refresh")
    response_data = response.json_body

    assert response.status_code == 400
    assert response_data == {
        "Code": "BadRequestError",
        "Message": "No refresh token specified in Authorization header",
    }


def test_user_can_revoke_refresh_tokens(
    test_client: Client, registered_user: User, refresh_token: str, access_token: str
) -> None:
    headers = {"Authorization": f"Bearer {access_token}"}
    response = test_client.http.post("/tokens/revoke", headers=headers)

    assert response.status_code == 204
    assert user_service._user_data_access.get(pk=registered_user.pk, sk=registered_user.sk).refresh_token_jtis == []


def test_user_cannot_revoke_refresh_tokens_without_access_token(
    test_client: Client, registered_user: User, refresh_token: str
) -> None:
    response = test_client.http.post("/tokens/revoke")
    assert response.status_code == 401
