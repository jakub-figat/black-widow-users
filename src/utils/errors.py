from chalice import Response
from pydantic import ValidationError


def get_response_from_pydantic_error(error: ValidationError) -> Response:
    return Response(body={"detail": error.errors()}, status_code=422)
