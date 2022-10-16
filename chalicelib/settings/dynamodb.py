from pydantic import BaseSettings, Field


class DynamoDBSettings(BaseSettings):
    dynamodb_table_name: str = Field(..., env="DYNAMODB_TABLE_NAME")
