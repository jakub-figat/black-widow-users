from src.models.user import User


class UserService:
    def __init__(self, user_data_access) -> None:
        self._user_data_access = user_data_access

    @classmethod
    def register_user(cls, user: User) -> User:
        pass
