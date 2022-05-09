from uuid import uuid4

import pytest
from mypy_boto3_dynamodb.service_resource import Table

from src.data_access.exceptions import AlreadyExists, DoesNotExist
from src.data_access.user import UserDynamoDBDataAccess
from src.models.user import User


@pytest.fixture
def user_data_access(dynamodb_testcase_table: Table) -> UserDynamoDBDataAccess:
    return UserDynamoDBDataAccess(table_name=dynamodb_testcase_table.table_name)


@pytest.fixture
def user_data_access_with_user_with_password(dynamodb_testcase_table: Table) -> UserDynamoDBDataAccess:
    data_access = UserDynamoDBDataAccess(table_name=dynamodb_testcase_table.table_name)
    data_access.create_user_with_password(email="janusz123@aa.pl", password="password12345")
    return data_access


@pytest.fixture
def user_data_access_with_user_inserted(dynamodb_testcase_table: Table) -> UserDynamoDBDataAccess:
    data_access = UserDynamoDBDataAccess(table_name=dynamodb_testcase_table.table_name)
    data_access.create(model=User(email="stach@op.pl"))
    return data_access


@pytest.fixture
def user_data_access_with_user_with_refresh_token_jti(dynamodb_testcase_table: Table) -> UserDynamoDBDataAccess:
    data_access = UserDynamoDBDataAccess(table_name=dynamodb_testcase_table.table_name)
    data_access.create(model=User(email="stach@op.pl", refresh_token_jtis=["fakejti"]))
    return data_access


@pytest.fixture
def user_data_access_with_many_users_inserted(dynamodb_testcase_table: Table) -> UserDynamoDBDataAccess:
    data_access = UserDynamoDBDataAccess(table_name=dynamodb_testcase_table.table_name)
    data_access.create_many(
        models=[
            User(email="stachu1@op.pl"),
            User(email="stachu2@op.pl"),
        ]
    )
    return data_access


def test_dynamodb_user_data_access_can_get_user(user_data_access_with_user_inserted: UserDynamoDBDataAccess) -> None:
    user = user_data_access_with_user_inserted.get(pk="user#stach@op.pl", sk="user#stach@op.pl")
    assert user == User(email="stach@op.pl")


def test_dynamodb_user_data_access_returns_none_when_user_does_not_exist(
    user_data_access: UserDynamoDBDataAccess,
) -> None:
    assert user_data_access.get(pk="user#doesnotexist", sk="user#doesnotexist") is None


def test_dynamodb_user_data_access_can_create_user(user_data_access: UserDynamoDBDataAccess) -> None:
    user = User(email="stachecki@op.pl")
    user_created = user_data_access.create(model=user)

    assert user == user_created


def test_dynamodb_user_data_access_raises_already_exists_if_email_exists(
    user_data_access_with_user_inserted: UserDynamoDBDataAccess,
) -> None:
    with pytest.raises(AlreadyExists):
        user_data_access_with_user_inserted.create(model=User(email="stach@op.pl"))


def test_dynamodb_user_data_access_can_create_many_users(user_data_access: UserDynamoDBDataAccess) -> None:
    users = user_data_access.create_many(
        models=[
            User(email="stachu5@op.pl"),
            User(email="stachu6@op.pl"),
        ]
    )

    assert users == [
        User(email="stachu5@op.pl"),
        User(email="stachu6@op.pl"),
    ]


def test_dynamodb_user_data_access_can_delete_user(
    user_data_access_with_user_inserted: UserDynamoDBDataAccess,
) -> None:
    user_data_access_with_user_inserted.delete(pk="user#stach@op.pl", sk="user#stach@op.pl")
    assert user_data_access_with_user_inserted.get(pk="user#stach@op.pl", sk="user#stach@op.pl") is None


def test_dynamodb_user_data_access_raises_does_not_exist_when_deleting_not_existing_item(
    user_data_access: UserDynamoDBDataAccess,
) -> None:
    with pytest.raises(DoesNotExist):
        user_data_access.delete(pk="abc", sk="def")


def test_dynamodb_user_data_access_can_register_user(user_data_access: UserDynamoDBDataAccess) -> None:
    user = user_data_access.create_user_with_password(email="register@op.pl", password="password1234567")

    user_from_db = user_data_access.get(pk="user#register@op.pl", sk="user#register@op.pl")
    assert user_from_db == user


def test_dynamodb_user_data_access_raises_already_exists_when_email_is_occupied(
    user_data_access_with_user_inserted: UserDynamoDBDataAccess,
) -> None:
    with pytest.raises(AlreadyExists):
        user_data_access_with_user_inserted.create_user_with_password(
            email="stach@op.pl", password="doesnotmakeadifference"
        )


def test_dynamodb_user_data_access_can_check_password(
    user_data_access_with_user_with_password: UserDynamoDBDataAccess,
) -> None:
    assert user_data_access_with_user_with_password.check_password(email="janusz123@aa.pl", password="password12345")


def test_dynamodb_user_data_access_raises_does_not_exist_when_checking_not_existing_user_password(
    user_data_access: UserDynamoDBDataAccess,
) -> None:
    with pytest.raises(DoesNotExist):
        user_data_access.check_password(email="doesnotexist", password="doesntmatter")


def test_dynamodb_user_data_access_can_add_refresh_token_jti(
    user_data_access_with_user_inserted: UserDynamoDBDataAccess,
) -> None:
    jti = str(uuid4())
    user_data_access_with_user_inserted.add_refresh_token_jti(User(email="stach@op.pl"), refresh_token_jti=jti)
    user: User = user_data_access_with_user_inserted.get(pk="user#stach@op.pl", sk="user#stach@op.pl")

    assert user.refresh_token_jtis == [jti]


def test_dynamodb_user_data_access_can_remove_refresh_token_jtis(
    user_data_access_with_user_with_refresh_token_jti: UserDynamoDBDataAccess,
) -> None:
    user_data_access_with_user_with_refresh_token_jti.delete_user_refresh_token_jtis(user=User(email="stach@op.pl"))
    user: User = user_data_access_with_user_with_refresh_token_jti.get(pk="user#stach@op.pl", sk="user#stach@op.pl")

    assert user.refresh_token_jtis == []
