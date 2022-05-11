import pytest
from mypy_boto3_dynamodb.service_resource import Table

from chalicelib.services import user_dynamodb_data_access


@pytest.fixture(scope="session", autouse=True)
def override_user_data_access_table(dynamodb_test_table: Table) -> None:
    prev_table = user_dynamodb_data_access._table
    user_dynamodb_data_access._table = dynamodb_test_table
    yield
    user_dynamodb_data_access._table = prev_table
