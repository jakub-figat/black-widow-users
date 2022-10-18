from abc import ABC, abstractmethod
from typing import Generic, Optional, Type, TypeVar

from pydantic import BaseModel


Model = TypeVar("Model", bound=BaseModel)
PK = TypeVar("PK")


class AbstractDataAccess(Generic[PK, Model], ABC):
    @property
    @abstractmethod
    def _model(self) -> Type[Model]:
        pass

    @abstractmethod
    def get(self, pk: PK, *args, **kwargs) -> Optional[Model]:
        raise NotImplementedError

    @abstractmethod
    def create(self, *, model: Model) -> Model:
        raise NotImplementedError

    @abstractmethod
    def create_many(self, *, models: list[Model]) -> list[Model]:
        raise NotImplementedError

    @abstractmethod
    def delete(self, pk: PK, *args, **kwargs) -> bool:
        raise NotImplementedError
