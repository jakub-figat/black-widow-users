import pytest
from mypy_boto3_dynamodb.service_resource import Table

from src.data_access.user import UserDynamoDBDataAccess


@pytest.fixture
def user_dynamodb_data_access(dynamodb_testcase_table: Table) -> UserDynamoDBDataAccess:
    return UserDynamoDBDataAccess(table_name=dynamodb_testcase_table.table_name)
