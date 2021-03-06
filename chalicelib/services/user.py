from chalice import BadRequestError

from chalicelib.data_access.exceptions import AlreadyExists
from chalicelib.data_access.user import UserDynamoDBDataAccess
from chalicelib.models.user import User, UserRegisterInput


class UserService:
    def __init__(self, user_data_access: UserDynamoDBDataAccess) -> None:
        self._user_data_access = user_data_access

    def register_user(self, input_model: UserRegisterInput) -> User:
        try:
            return self._user_data_access.create_user_with_password(
                email=input_model.email, password=input_model.password
            )
        except AlreadyExists as error:
            raise BadRequestError(str(error)) from error
