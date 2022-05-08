import json

import pytest
from chalice.test import Client
from mypy_boto3_dynamodb.service_resource import Table

from src.data_access.user import UserDynamoDBDataAccess
from src.models.user import User
from src.services import user_dynamodb_data_access


@pytest.fixture(scope="session", autouse=True)
def override_table(dynamodb_test_table: Table) -> None:
    prev_table = user_dynamodb_data_access._table
    user_dynamodb_data_access._table = dynamodb_test_table
    yield
    user_dynamodb_data_access._table = prev_table


@pytest.fixture
def user_data_access_with_user_inserted(dynamodb_testcase_table: Table) -> UserDynamoDBDataAccess:
    data_access = UserDynamoDBDataAccess(table_name=dynamodb_testcase_table.table_name)
    data_access.create(model=User(email="stach@op.pl"))
    return data_access


def test_register_user(test_client: Client, dynamodb_testcase_table: Table) -> None:
    request_data = {"email": "stachmen@op.pl", "password": "abcdefg1234", "password_again": "abcdefg1234"}
    response = test_client.http.post(
        "/users/register", body=json.dumps(request_data), headers={"Content-Type": "application/json"}
    )
    response_data = response.json_body

    assert response.status_code == 201
    assert response_data["email"] == "stachmen@op.pl"


def test_register_users_returns_bad_request_when_email_is_occupied(
    test_client: Client, user_data_access_with_user_inserted: UserDynamoDBDataAccess
) -> None:
    request_data = {"email": "stach@op.pl", "password": "abcdefg1234", "password_again": "abcdefg1234"}

    response = test_client.http.post(
        "/users/register", body=json.dumps(request_data), headers={"Content-Type": "application/json"}
    )
    response_data = response.json_body
    assert response_data == {"Code": "BadRequestError", "Message": "User with email stach@op.pl already exists"}
    assert response.status_code == 400
