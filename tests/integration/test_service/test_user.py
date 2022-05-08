import pytest
from chalice import BadRequestError
from mypy_boto3_dynamodb.service_resource import Table

from src.data_access.user import UserDynamoDBDataAccess
from src.models.user import UserRegisterInput
from src.services.user import UserService


@pytest.fixture
def user_dynamodb_data_access(dynamodb_testcase_table: Table) -> UserDynamoDBDataAccess:
    return UserDynamoDBDataAccess(table_name=dynamodb_testcase_table.table_name)


@pytest.fixture
def user_service(user_dynamodb_data_access: UserDynamoDBDataAccess) -> UserService:
    return UserService(user_data_access=user_dynamodb_data_access)


def test_user_service_can_create_user_with_password(
    user_service: UserService, user_dynamodb_data_access: UserDynamoDBDataAccess
) -> None:
    user = user_service.register_user(
        input_model=UserRegisterInput(
            email="stachecki@op.pl", password="asdasdasd1234", password_again="asdasdasd1234"
        )
    )
    user_in_db = user_dynamodb_data_access.get(pk="user#stachecki@op.pl", sk="user#stachecki@op.pl")

    assert user == user_in_db


def test_user_service_raises_bad_request_error_when_email_is_occupied(user_service: UserService) -> None:
    user_service.register_user(
        input_model=UserRegisterInput(
            email="stachecki@op.pl", password="asdasdasd1234", password_again="asdasdasd1234"
        )
    )

    with pytest.raises(BadRequestError):
        user_service.register_user(
            input_model=UserRegisterInput(
                email="stachecki@op.pl", password="asdasdasd1234", password_again="asdasdasd1234"
            )
        )