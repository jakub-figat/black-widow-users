from abc import ABC, abstractmethod
from typing import Optional, TypeVar, Generic, Type

import boto3
from mypy_boto3_dynamodb import DynamoDBServiceResource


from src.data_access.abstract import AbstractDataAccess, PK
from src.models.dynamodb import DynamoDBBaseModel
from src.settings import settings


SK = TypeVar("SK")


class DynamoDBDataAccess(Generic[SK], AbstractDataAccess[PK, DynamoDBBaseModel], ABC):
    def __init__(self, table_name: str) -> None:
        dynamodb: DynamoDBServiceResource = boto3.resource("dynamodb", region_name=settings.region)
        self._table = dynamodb.Table(table_name)

    @property
    @abstractmethod
    def _model(self) -> Type[DynamoDBBaseModel]:
        raise NotImplementedError

    def get(self, *, pk: PK, sk: Optional[SK] = None) -> Optional[DynamoDBBaseModel]:
        key = {"PK": {"S": pk}}
        if sk is not None:
            key["SK"] = {"S": sk}

        return self._model.from_dynamodb(self._table.get_item(Key=key))

    def get_many(self, **kwargs) -> list[DynamoDBBaseModel]:
        pass

    def create(self, *, model: DynamoDBBaseModel) -> DynamoDBBaseModel:
        pass

    def create_many(self, *, models: list[DynamoDBBaseModel]) -> list[DynamoDBBaseModel]:
        pass

    def update(self, *, model: DynamoDBBaseModel) -> DynamoDBBaseModel:
        pass

    def update_many(self, *, models: list[DynamoDBBaseModel]) -> DynamoDBBaseModel:
        raise NotImplementedError

    def delete(self, *, pk: PK) -> bool:
        pass

    def delete_many(self, *, pks: list[PK]) -> int:
        pass
