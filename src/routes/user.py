from fastapi import APIRouter, Depends, status

from src.deps.user import get_request_user
from src.models.user import User, UserRegisterInput
from src.schemas.user import UserOutputSchema
from src.services import user_service


user_router = APIRouter(tags=["users"])


@user_router.post("/register/", status_code=status.HTTP_201_CREATED, response_model=UserOutputSchema)
def register_user(input_schema: UserRegisterInput) -> UserOutputSchema:
    return user_service.register_user(input_model=input_schema)


@user_router.get("/me/", status_code=status.HTTP_200_OK, response_model=UserOutputSchema)
def get_current_user(user: User = Depends(get_request_user)) -> UserOutputSchema:
    return user
