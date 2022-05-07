from botocore.exceptions import ClientError
from chalice import BadRequestError

from src.data_access.user import UserDynamoDBDataAccess
from src.models.user import User, UserRegisterInput


class UserService:
    def __init__(self, user_data_access: UserDynamoDBDataAccess) -> None:
        self._user_data_access = user_data_access

    def register_user(self, input_model: UserRegisterInput) -> User:
        try:
            return self._user_data_access.create_user_with_password(email=input_model.email, password=input_model.password)
        except ClientError as error:
            # TODO: this looks shitty
            if error.response["Error"]["Code"] == "ConditionalCheckFailedException":
                raise BadRequestError("Email already exists.")

