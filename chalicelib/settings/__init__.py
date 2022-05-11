from chalicelib.settings.aws import AWSSettings
from chalicelib.settings.dynamodb import DynamoDBSettings
from chalicelib.settings.security import SecuritySettings


class Settings(SecuritySettings, AWSSettings, DynamoDBSettings):
    pass


settings = Settings()
