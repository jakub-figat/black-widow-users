from src.models.abstract import BaseSchema


class TokenPairOutput(BaseSchema):
    access_token: str
    refresh_token: str
