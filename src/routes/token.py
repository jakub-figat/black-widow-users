from chalice import BadRequestError, Response, UnauthorizedError

from app import app
from src.models.user import UserLoginInput
from src.services import token_service


@app.route("/tokens", methods=["POST"])
def get_token_pair() -> dict[str, str]:
    login_input = UserLoginInput(**app.current_request.json_body)
    return token_service.create_token_pair_by_login(login_input=login_input).dict()


@app.route("/tokens/refresh", methods=["POST"])
def get_token_pair_by_refresh() -> dict[str, str]:
    if (auth_header := app.current_request.headers.get("Authorization")) is None:
        raise BadRequestError("No refresh token specified in Authorization header")

    token = token_service.parse_token_from_header(header=auth_header)
    return token_service.create_token_pair_by_refresh(refresh_token=token)


@app.route("/tokens/revoke")
def revoke_refresh_tokens() -> Response:
    if (user := app.current_request.user) is None:
        raise UnauthorizedError("Authentication credentials were not provided")

    token_service.revoke_user_refresh_tokens(user=user)
    return Response(body=None, status_code=204)
