from typing import Any

from aws_lambda_powertools.logging import Logger

from src.services import TokenService
from src.services.token import TokenServiceException


logger = Logger()


@logger.inject_lambda_context(log_event=True)
def authorize_from_jwt(event: dict[str, Any], context: Any) -> dict[str, Any]:
    authorization_header = event["headers"].get("Authorization")
    if authorization_header is None:
        return {"isAuthorized": False}

    try:
        token = TokenService.parse_token_from_header(header=authorization_header)
        token_data = TokenService.decode_token(token=token)
        return {"isAuthorized": True, "context": {"user": token_data["sub"]}}
    except TokenServiceException as exc:
        logger.warning("TokenException: %s" % str(exc))
        return {"isAuthorized": False}
