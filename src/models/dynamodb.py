from pydantic import BaseModel


class DynamoDBBaseModel(BaseModel):
    PK: str
    SK: str
