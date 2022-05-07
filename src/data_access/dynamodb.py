from abc import ABC, abstractmethod
from typing import Generic, Optional, Type, TypeVar

import boto3
from boto3.dynamodb.conditions import Key
from mypy_boto3_dynamodb import DynamoDBServiceResource

from src.data_access.abstract import PK, AbstractDataAccess
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

    def get(self, *, pk: PK, sk: SK) -> Optional[DynamoDBBaseModel]:
        key = {"PK": pk, "SK": sk}

        response = self._table.get_item(Key=key)
        if (item := response.get("Item")) is not None:
            return self._model(**item)

        return None

    def get_many(self, pk: PK) -> list[DynamoDBBaseModel]:
        expression = Key("PK").eq(pk)

        items = self._table.query(KeyConditionExpression=expression)["Items"]
        return [self._model(**item) for item in items]

    def create(self, *, model: DynamoDBBaseModel) -> DynamoDBBaseModel:
        self._table.put_item(Item=model.dict(), ConditionExpression="attribute_not_exists(SK)")
        return model

    def create_many(self, *, models: list[DynamoDBBaseModel]) -> list[DynamoDBBaseModel]:
        with self._table.batch_writer() as batch:
            for model in models:
                batch.put_item(Item=model.dict())

    def delete(self, *, pk: PK, sk: SK) -> bool:
        key = {"PK": pk, "SK": sk}
        result = self._table.delete_item(Key=key)

        return result
