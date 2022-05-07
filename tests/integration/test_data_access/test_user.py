import pytest
from mypy_boto3_dynamodb.service_resource import Table

from src.data_access.user import UserDynamoDBDataAccess
from src.models.user import User


@pytest.fixture
def user_data_access(dynamodb_testcase_table: Table) -> UserDynamoDBDataAccess:
    return UserDynamoDBDataAccess(table_name=dynamodb_testcase_table.table_name)


@pytest.fixture
def user_data_access_with_user_inserted(dynamodb_testcase_table: Table) -> UserDynamoDBDataAccess:
    data_access = UserDynamoDBDataAccess(table_name=dynamodb_testcase_table.table_name)
    data_access.create(model=User(PK="testuser", SK="user#testuser"))
    return data_access


@pytest.fixture
def user_data_access_with_many_users_inserted(dynamodb_testcase_table: Table) -> UserDynamoDBDataAccess:
    data_access = UserDynamoDBDataAccess(table_name=dynamodb_testcase_table.table_name)
    data_access.create_many(
        models=[
            User(PK="testuser", SK="user#testuser1"),
            User(PK="testuser", SK="user#testuser2"),
        ]
    )
    return data_access


def test_dynamodb_user_data_access_can_get_user(user_data_access_with_user_inserted: UserDynamoDBDataAccess) -> None:
    user = user_data_access_with_user_inserted.get(pk="testuser", sk="user#testuser")
    assert user == User(PK="testuser", SK="user#testuser")


def test_dynamodb_user_data_access_can_get_many_users(
    user_data_access_with_many_users_inserted: UserDynamoDBDataAccess,
) -> None:
    users = user_data_access_with_many_users_inserted.get_many(pk="testuser")
    assert users == [
        User(PK="testuser", SK="user#testuser1"),
        User(PK="testuser", SK="user#testuser2"),
    ]


def test_dynamodb_user_data_access_can_create_user(user_data_access: UserDynamoDBDataAccess) -> None:
    user = User(PK="stachu", SK="user#stachu")
    user_created = user_data_access.create(model=user)

    assert user == user_created


def test_dynamodb_user_data_access_can_create_many_users(user_data_access: UserDynamoDBDataAccess) -> None:
    users = user_data_access.create_many(
        models=[
            User(PK="testuser", SK="user#testuser1"),
            User(PK="testuser", SK="user#testuser2"),
        ]
    )

    assert users == [
        User(PK="testuser", SK="user#testuser1"),
        User(PK="testuser", SK="user#testuser2"),
    ]


def test_dynamodb_user_data_access_can_delete_user(
    user_data_access_with_user_inserted: UserDynamoDBDataAccess,
) -> None:
    user_data_access_with_user_inserted.delete(pk="testuser", sk="user#testuser")
    assert user_data_access_with_user_inserted.get(pk="testuser", sk="user#testuser") is None
