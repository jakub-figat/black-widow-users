from fastapi import APIRouter, Depends, Response, status
from fastapi.security import OAuth2PasswordBearer

from src.data_access.exceptions import DoesNotExist
from src.models.token import TokenPairOutput
from src.schemas.user import UserLoginInput
from src.services import token_service, user_dynamodb_data_access


token_router = APIRouter(tags=["tokens"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/tokens")


@token_router.post("/", status_code=status.HTTP_200_OK, response_model=TokenPairOutput)
def get_token_pair(login_input: UserLoginInput) -> TokenPairOutput:
    return token_service.create_token_pair_by_login(login_input=login_input)


@token_router.post("/refresh/", status_code=status.HTTP_200_OK, response_model=TokenPairOutput)
def get_token_pair_by_refresh(token: str = Depends(oauth2_scheme)) -> TokenPairOutput:
    return token_service.create_token_pair_by_refresh(refresh_token=token)


@token_router.post("/revoke/", status_code=status.HTTP_204_NO_CONTENT)
def revoke_refresh_tokens(token: str = Depends(oauth2_scheme)) -> Response:
    email = token_service.decode_token(token=token)["sub"]
    user = user_dynamodb_data_access.get(pk=f"user#{email}", sk=f"user#{email}")
    if user is None:
        raise DoesNotExist(f"User with email {email} not found")

    token_service.revoke_user_refresh_tokens(user=user)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
