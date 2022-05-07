from typing import Type

from src.data_access.dynamodb import DynamoDBDataAccess
from src.models.user import User


class UserDynamoDBDataAccess(DynamoDBDataAccess[str]):
    @property
    def _model(self) -> Type[User]:
        return User
