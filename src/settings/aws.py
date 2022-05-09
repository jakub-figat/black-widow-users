from pydantic import BaseSettings


class AWSSettings(BaseSettings):
    aws_access_key: str
    aws_secret_key: str
    region: str = "eu-central-1"
