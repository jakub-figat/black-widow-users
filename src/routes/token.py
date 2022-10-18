from fastapi import APIRouter, Response, status

from src.models.token import TokenPairOutput
from src.models.user import User
from src.schemas.user import UserLoginInput
from src.services import token_service


token_router = APIRouter(tags=["tokens"])


@token_router.post("/", status_code=status.HTTP_200_OK, response_model=TokenPairOutput)
def get_token_pair(login_input: UserLoginInput) -> TokenPairOutput:
    return token_service.create_token_pair_by_login(login_input=login_input)


@token_router.post("/tokens/refresh", status_code=status.HTTP_200_OK, response_model=TokenPairOutput)
def get_token_pair_by_refresh() -> TokenPairOutput:
    # TODO: dependency that checks if token is contained by request
    # if (auth_header := app.current_request.headers.get("Authorization")) is None:
    #     raise BadRequestError("No refresh token specified in Authorization header")

    token = token_service.parse_token_from_header(header="dupsko")
    return token_service.create_token_pair_by_refresh(refresh_token=token)


@token_router.post("/tokens/revoke", status_code=status.HTTP_204_NO_CONTENT)
def revoke_refresh_tokens() -> Response:
    # TODO: check if user is authorized
    email = "from dependency?"

    token_service.revoke_user_refresh_tokens(user=User(email=email))
    return Response(status_code=204)
