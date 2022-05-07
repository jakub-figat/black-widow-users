from src.data_access.user import UserDynamoDBDataAccess
from src.services.user import UserService
from src.settings import settings


user_dynamodb_data_access = UserDynamoDBDataAccess(table_name=settings.table_name)
user_service = UserService(user_data_access=user_dynamodb_data_access)