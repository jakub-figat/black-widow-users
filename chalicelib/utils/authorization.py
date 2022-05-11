from chalice import AuthResponse
from chalice.app import AuthRequest

from app import app
from chalicelib.services import token_service


@app.authorizer()
def jwt_auth(auth_request: AuthRequest) -> AuthResponse:
    user = token_service.authenticate_user_from_header(auth_request.token)

    return AuthResponse(routes=["*"], principal_id=user.email)
