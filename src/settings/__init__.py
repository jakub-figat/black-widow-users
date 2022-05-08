from src.settings.aws import AWSSettings
from src.settings.dynamodb import DynamoDBSettings
from src.settings.security import SecuritySettings


class Settings(SecuritySettings, AWSSettings, DynamoDBSettings):
    pass


settings = Settings()
