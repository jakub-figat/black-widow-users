from pydantic import BaseSettings


class DynamoDBSettings(BaseSettings):
    table_name: str
