from chalicelib.data_access.user import UserDynamoDBDataAccess
from chalicelib.services.token import TokenService
from chalicelib.services.user import UserService
from chalicelib.settings import settings


user_dynamodb_data_access = UserDynamoDBDataAccess(table_name=settings.dynamodb_table_name)

user_service = UserService(user_data_access=user_dynamodb_data_access)
token_service = TokenService(user_data_access=user_dynamodb_data_access)
