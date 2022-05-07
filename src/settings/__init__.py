from src.settings.aws import AWSSettings
from src.settings.dynamodb import DynamoDBSettings


class Settings(AWSSettings, DynamoDBSettings):
    pass


settings = Settings()
