import datetime as dt

import pytest

from src.data_access.user import UserDynamoDBDataAccess
from src.models.user import User
from src.settings import settings


@pytest.fixture
def user_data_access() -> UserDynamoDBDataAccess:
    return UserDynamoDBDataAccess(table_name=settings.table_name)


@pytest.fixture
def user_data_access_with_user_inserted() -> UserDynamoDBDataAccess:
    data_access = UserDynamoDBDataAccess(table_name=settings.table_name)
    data_access.create(model=User(PK="testuser", SK="user#testuser", date_of_birth=dt.datetime(2022, 1, 1)))


def test_dynamodb_user_data_access_can_create_user(user_data_access: UserDynamoDBDataAccess) -> None:
    user = User(PK="stachu", SK="user#stachu", date_of_birth=dt.datetime(2020, 1, 1))
    user_created = user_data_access.create(model=user)

    assert user == user_created


def test_dynamodb_user_data_access_can_get_user(user_data_access_with_user_inserted: UserDynamoDBDataAccess) -> None:
    user = user_data_access_with_user_inserted.get(pk="testuser", sk="user#testuser")
    assert user == User(PK="testuser", SK="user#testuser", date_of_birth=dt.datetime(2022, 1, 1))
