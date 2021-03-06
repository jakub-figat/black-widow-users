from typing import Optional, Type

from botocore.exceptions import ClientError

from chalicelib.data_access.dynamodb import DynamoDBDataAccess
from chalicelib.data_access.exceptions import AlreadyExists, DoesNotExist
from chalicelib.models.user import User
from chalicelib.utils.password import hash_password, verify_password


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

    def check_password(self, email: str, password: str) -> bool:
        user_key = f"user#{email}"
        response = self._table.get_item(Key={"PK": user_key, "SK": user_key})

        if (user_item := response.get("Item")) is None:
            raise DoesNotExist(f"User with email {email} does not exist")

        return verify_password(password, user_item["password"])

    def add_refresh_token_jti(self, user: User, refresh_token_jti: str) -> None:
        user_model: Optional[User] = self.get(pk=user.pk, sk=user.pk)

        if user_model is None:
            raise DoesNotExist(f"User with email {user.email} does not exist")

        user_model.refresh_token_jtis.append(refresh_token_jti)
        self._table.put_item(Item=user_model.to_item())

    def delete_user_refresh_token_jtis(self, user: User) -> None:
        user_model: Optional[User] = self.get(pk=user.pk, sk=user.sk)

        if user_model is None:
            raise DoesNotExist(f"User with email {user.email} does not exist")

        user_model.refresh_token_jtis = []
        self._table.put_item(Item=user_model.to_item())
