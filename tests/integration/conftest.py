import random

import boto3
import pytest
from chalice.test import Client
from mypy_boto3_dynamodb.service_resource import DynamoDBServiceResource, Table

from app import app
from src.settings import settings


@pytest.fixture(scope="session")
def dynamodb_test_table() -> Table:
    dynamodb: DynamoDBServiceResource = boto3.resource(
        "dynamodb",
        region_name=settings.region,
        aws_access_key_id=settings.aws_access_key,
        aws_secret_access_key=settings.aws_secret_key,
    )
    test_table = dynamodb.create_table(
        TableName=f"dynamodb_test_table_{random.randint(1, 10000)}",
        AttributeDefinitions=[
            {"AttributeName": "PK", "AttributeType": "S"},
            {
                "AttributeName": "SK",
                "AttributeType": "S",
            },
        ],
        KeySchema=[{"AttributeName": "PK", "KeyType": "HASH"}, {"AttributeName": "SK", "KeyType": "RANGE"}],
        BillingMode="PAY_PER_REQUEST",
    )

    test_table.wait_until_exists()

    yield test_table
    test_table.delete()


@pytest.fixture
def dynamodb_testcase_table(dynamodb_test_table: Table) -> Table:
    scan = dynamodb_test_table.scan()
    with dynamodb_test_table.batch_writer() as batch:
        for item in scan["Items"]:
            batch.delete_item(Key={"PK": item["PK"], "SK": item["SK"]})

    yield dynamodb_test_table

    scan = dynamodb_test_table.scan()
    with dynamodb_test_table.batch_writer() as batch:
        for item in scan["Items"]:
            batch.delete_item(Key={"PK": item["PK"], "SK": item["SK"]})


@pytest.fixture
def test_client() -> Client:
    with Client(app=app) as client:
        yield client
