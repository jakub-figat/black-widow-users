from pydantic.fields import Field
from pydantic.networks import EmailStr

from src.models.abstract import BaseSchema


class UserOutputSchema(BaseSchema):
    email: str


class UserLoginInput(BaseSchema):
    email: EmailStr
    password: str = Field(..., min_length=8, max_length=32)
