from typing import Any

from pydantic import BaseModel


class DynamoDBBaseModel(BaseModel):
    PK: str

    @classmethod
    def from_dynamodb(cls, response: dict[str, dict[str, Any]]) -> "DynamoDBBaseModel":
        item = response["Item"]
        model_dict = {}

        for field, field_dict in item.items():
            value, *_ = list(field_dict.values())
            model_dict[field] = value

        return cls(**model_dict)

    @classmethod
    def to_dynamodb(cls) -> dict[str, dict[str, Any]]:
        pass
