from typing import Any, Optional


def generate_authorizer_policy_response(
    principal_id: Optional[str],
    method_arn: str,
) -> dict[str, Any]:
    if principal_id is None:
        return {
            "principalId": "Unknown",
            "policyDocument": {
                "Version": "2012-10-17",
                "Statement": [{"Action": "execute-api:Invoke", "Effect": "Deny", "Resource": method_arn}],
            },
        }

    return {
        "principalId": principal_id,
        "policyDocument": {
            "Version": "2012-10-17",
            "Statement": [{"Action": "execute-api:Invoke", "Effect": "Allow", "Resource": method_arn}],
        },
    }
