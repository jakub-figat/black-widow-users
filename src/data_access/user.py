from typing import Optional, Type

from botocore.exceptions import ClientError

from src.data_access.dynamodb import DynamoDBDataAccess
from src.data_access.exceptions import AlreadyExists, DoesNotExist
from src.models.user import User
from src.utils.password import hash_password


class UserDynamoDBDataAccess(DynamoDBDataAccess[str]):
    @property
    def _model(self) -> Type[User]:
        return User

    def create_user_with_password(self, email: str, password: str) -> User:
        user_key = f"user#{email}"
        user_item = {"PK": user_key, "SK": user_key, "password": hash_password(password=password)}
        try:
            self._table.put_item(Item=user_item, ConditionExpression="attribute_not_exists(PK)")
        except ClientError as error:
            if error.response["Error"]["Code"] == "ConditionalCheckFailedException":
                raise AlreadyExists(f"User with email {email} already exists") from error
            raise error

        return User(email=email)

    def add_refresh_token_jti(self, user: User, refresh_token_jti: str) -> None:
        user_item: Optional[User] = self.get(pk=user.pk, sk=user.pk)

        if user_item is None:
            raise DoesNotExist(f"User with email {user.email} does not exist")

        user_item.refresh_token_jtis.append(refresh_token_jti)
        self._table.put_item(Item=user_item)
