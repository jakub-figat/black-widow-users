from pydantic import BaseSettings


class AWSSettings(BaseSettings):
    access_key: str
    secret_key: str
    region: str = "eu-central-1"

    @property
    def dynamodb_url(self) -> str:
        return (
            f"amazondynamodb:///?Access Key={self.access_key}&Secret Key={self.secret_key}"
            f"&Domain=amazonaws.com&Region={self.region}"
        )
