import datetime as dt

from src.models.dynamodb import DynamoDBBaseModel


class User(DynamoDBBaseModel):
    date_of_birth: dt.datetime
