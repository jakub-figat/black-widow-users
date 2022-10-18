import pytest
from fastapi import status
from fastapi.testclient import TestClient
from mypy_boto3_dynamodb.service_resource import Table

from src.data_access.user import UserDynamoDBDataAccess
from src.models.user import User


@pytest.fixture
def user_data_access_with_user_inserted(dynamodb_testcase_table: Table) -> UserDynamoDBDataAccess:
    data_access = UserDynamoDBDataAccess(table_name=dynamodb_testcase_table.table_name)
    data_access.create(model=User(email="stach@op.pl", password="some_password12345"))
    return data_access


def test_register_user(test_client: TestClient, dynamodb_testcase_table: Table) -> None:
    request_data = {"email": "stachmen@op.pl", "password": "abcdefg1234", "password_again": "abcdefg1234"}
    response = test_client.post("/users/register", json=request_data, headers={"Content-Type": "application/json"})
    response_data = response.json()

    assert response.status_code == status.HTTP_201_CREATED
    assert response_data["email"] == "stachmen@op.pl"


def test_register_users_returns_bad_request_when_email_is_occupied(
    test_client: TestClient, user_data_access_with_user_inserted: UserDynamoDBDataAccess
) -> None:
    request_data = {"email": "stach@op.pl", "password": "abcdefg1234", "password_again": "abcdefg1234"}

    response = test_client.post("/users/register", json=request_data, headers={"Content-Type": "application/json"})
    response_data = response.json()
    assert response_data == {"detail": "User with email stach@op.pl already exists"}
    assert response.status_code == status.HTTP_400_BAD_REQUEST
