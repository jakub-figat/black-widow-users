from chalice import Response

from app import app
from src.models.user import UserRegisterInput
from src.services import user_service


@app.route("/users/register", methods=["POST"])
def register_user() -> Response:
    input_model = UserRegisterInput(**app.current_request.json_body)
    user = user_service.register_user(input_model=input_model).dict()
    return Response(body=user, status_code=201)
