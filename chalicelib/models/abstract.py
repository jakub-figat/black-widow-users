from abc import ABC, abstractmethod
from typing import Any

from pydantic import BaseModel


class DynamoDBBaseModel(BaseModel, ABC):
    @classmethod
    @abstractmethod
    def from_item(cls, item: dict[str, Any]) -> "DynamoDBBaseModel":
        raise NotImplementedError

    @abstractmethod
    def to_item(self) -> dict[str, Any]:
        raise NotImplementedError

    @property
    @abstractmethod
    def pk(self) -> str:
        raise NotImplementedError

    @property
    @abstractmethod
    def sk(self) -> str:
        raise NotImplementedError
