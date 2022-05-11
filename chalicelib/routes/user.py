from chalice import Response
from pydantic import ValidationError

from app import app
from chalicelib.models.user import UserRegisterInput
from chalicelib.services import user_service
from chalicelib.utils.errors import get_response_from_pydantic_error


@app.route("/users/register", methods=["POST"])
def register_user() -> Response:
    json_body = app.current_request.json_body or {}
    try:
        input_model = UserRegisterInput(**json_body)
    except ValidationError as error:
        return get_response_from_pydantic_error(error=error)

    user = user_service.register_user(input_model=input_model).dict()
    return Response(body=user, status_code=201)
