from typing import Any

from app import app
from src.instances import user_service
from src.models.user import UserRegisterInput


@app.route("/users", methods=["GET"])
def get_users() -> list[dict[str, Any]]:
    return [{"email": "smokegum@op.pl"}]


@app.route("/users/register", methods=["POST"])
def register_user() -> dict[str, str]:
    input_model = UserRegisterInput(**app.current_request.json_body)
    return user_service.register_user(input_model=input_model).dict()
