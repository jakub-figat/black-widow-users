from typing import Any

from pydantic import BaseModel

from src.models.abstract import DynamoDBBaseModel


class User(DynamoDBBaseModel):
    email: str

    @classmethod
    def from_item(cls, item: dict[str, Any]) -> "User":
        _, email = item["PK"].split("#")
        return cls(email=email)

    def to_item(self) -> dict[str, Any]:
        key = f"user#{self.email}"
        return {"PK": key, "SK": key}


class UserLoginInput(BaseModel):
    username: str
    password: str
