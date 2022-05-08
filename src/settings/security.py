from pydantic import BaseSettings


class SecuritySettings(BaseSettings):
    secret_key: str
    access_token_lifetime_in_minutes: int = 60
    refresh_token_lifetime_in_minutes: int = 60 * 24 * 30
