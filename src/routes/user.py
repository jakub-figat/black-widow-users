from app import app
from src.services.user import UserService


@app.route("/register")
def register_user() -> dict[str, str]:
    pass
