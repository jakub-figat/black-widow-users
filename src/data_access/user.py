from typing import Type

from src.data_access.dynamodb import DynamoDBDataAccess
from src.models.user import User


class UserDynamoDBDataAccess(DynamoDBDataAccess[str, User]):
    @property
    def _model(self) -> Type[User]:
        return User
