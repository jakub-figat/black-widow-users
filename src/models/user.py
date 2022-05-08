from typing import Any

from pydantic import BaseModel, EmailStr, Field, validator

from src.models.abstract import DynamoDBBaseModel


class User(DynamoDBBaseModel):
    email: str

    @classmethod
    def from_item(cls, item: dict[str, Any]) -> "User":
        _, email = item["PK"].split("#")
        return cls(email=email)

    def to_item(self) -> dict[str, Any]:
        key = self.pk
        return {"PK": key, "SK": key}

    @property
    def pk(self) -> str:
        return f"user#{self.email}"

    @property
    def sk(self) -> str:
        return f"user#{self.email}"


class UserRegisterInput(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=8, max_length=32)
    password_again: str = Field(..., min_length=8, max_length=32)

    @validator("password_again")
    def validate_password_again(cls, password_again: str, values: dict[str, Any]) -> str:
        if password_again != values["password"]:
            raise ValueError("Passwords do not match.")

        return password_again


class UserLoginInput(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=8, max_length=32)
