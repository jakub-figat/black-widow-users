from pydantic import BaseSettings, Field


class SecuritySettings(BaseSettings):
    secret_key: str = Field(..., env="SECRET_KEY")
    access_token_lifetime_in_minutes: int = Field(60, env="ACCESS_TOKEN_LIFETIME_MINUTES")
    refresh_token_lifetime_in_minutes: int = Field(60 * 24 * 30, env="REFRESH_TOKEN_LIFETIME_MINUTES")
