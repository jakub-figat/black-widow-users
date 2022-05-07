from pydantic import BaseSettings


class AWSSettings(BaseSettings):
    access_key: str
    secret_key: str
    region: str = "eu-central-1"
