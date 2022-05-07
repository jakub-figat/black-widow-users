from pydantic import BaseModel, Field


class User(BaseModel):
    username: str = Field(..., min_length=8, max_length=50)
