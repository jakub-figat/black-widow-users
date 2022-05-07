from typing import Type

from src.data_access.dynamodb import DynamoDBDataAccess
from src.models.user import User
from src.utils.password import hash_password


class UserDynamoDBDataAccess(DynamoDBDataAccess[str]):
    @property
    def _model(self) -> Type[User]:
        return User

    def create_user_with_password(self, email: str, password: str) -> User:
        user_key = f"user#{email}"
        user_item = {"PK": user_key, "SK": user_key, "password": hash_password(password=password)}

        # TODO: error handling
        self._table.put_item(Item=user_item, ConditionExpression="attribute_not_exists(PK)")

        return User(email=email)
