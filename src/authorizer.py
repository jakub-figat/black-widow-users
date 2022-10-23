from typing import Any

from aws_lambda_powertools.logging import Logger

from src.services import TokenService
from src.services.token import TokenServiceException
from src.utils.authorization import generate_authorizer_policy_response


logger = Logger()


@logger.inject_lambda_context(log_event=True)
def authorize_from_jwt(event: dict[str, Any], context: Any) -> dict[str, Any]:
    method_arn = event["methodArn"]
    authorization_header = event["headers"].get("Authorization")
    if authorization_header is None:
        return generate_authorizer_policy_response(principal_id=None, method_arn=method_arn)

    try:
        token = TokenService.parse_token_from_header(header=authorization_header)
        token_data = TokenService.decode_token(token=token)

        return generate_authorizer_policy_response(principal_id=token_data["sub"], method_arn=method_arn)

    except TokenServiceException as exc:
        logger.warning(str(exc))
        return generate_authorizer_policy_response(principal_id=None, method_arn=method_arn)
