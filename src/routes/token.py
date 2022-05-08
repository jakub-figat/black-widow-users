from chalice import Response

from app import app


@app.route("/tokens", methods=["POST"])
def get_token_pair() -> dict[str, str]:
    pass


@app.route("/tokens/refresh", methods=["POST"])
def get_token_pair_by_refresh() -> dict[str, str]:
    pass


@app.route("/tokens/revoke")
def revoke_refresh_tokens() -> Response:
    pass
