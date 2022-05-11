from chalice import BadRequestError, Response
from pydantic import ValidationError

from app import app
from chalicelib.models.user import User, UserLoginInput
from chalicelib.services import token_service
from chalicelib.utils.authorization import jwt_auth
from chalicelib.utils.errors import get_response_from_pydantic_error


@app.route("/tokens", methods=["POST"])
def get_token_pair() -> dict[str, str]:
    json_body = app.current_request.json_body or {}
    try:
        login_input = UserLoginInput(**json_body)
    except ValidationError as error:
        return get_response_from_pydantic_error(error=error)

    return token_service.create_token_pair_by_login(login_input=login_input).dict()


@app.route("/tokens/refresh", methods=["POST"])
def get_token_pair_by_refresh() -> dict[str, str]:
    if (auth_header := app.current_request.headers.get("Authorization")) is None:
        raise BadRequestError("No refresh token specified in Authorization header")

    token = token_service.parse_token_from_header(header=auth_header)
    return token_service.create_token_pair_by_refresh(refresh_token=token).dict()


@app.route("/tokens/revoke", methods=["POST"], authorizer=jwt_auth)
def revoke_refresh_tokens() -> Response:
    email = app.current_request.context["authorizer"]["principalId"]

    token_service.revoke_user_refresh_tokens(user=User(email=email))
    return Response(body=None, status_code=204)
