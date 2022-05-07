from typing import Optional
from uuid import UUID

from src.data_access.user import UserDynamoDBDataAccess


class TokenService:
    def __init__(self, user_data_access: UserDynamoDBDataAccess) -> None:
        self._user_data_access = user_data_access

    def _validate_user(self, user: Optional[User], token_input: TokenInput) -> list[Error]:
        errors = []
        if user is None or not password_context.verify(token_input.api_key, user.api_key_hash):
            errors.append(InvalidCredentials(message="Invalid credentials."))

        return errors

    async def _create_token_pair(self, user: User) -> TokenPair:
        token_pair = {
            "access_token": self._auth_jwt.create_access_token(subject=user.name),
            "refresh_token": self._auth_jwt.create_refresh_token(subject=user.name),
        }

        decoded_refresh_token = self._auth_jwt.get_raw_jwt(encoded_token=token_pair["refresh_token"])
        await self._refresh_token_data_access.create(
            input_schema=TokenInputSchema(user_id=user.id, jti=UUID(decoded_refresh_token["jti"]))
        )

        return TokenPair(**token_pair)

    async def _revoke_refresh_token(self, refresh_token: Optional[str] = None) -> list[Error]:
        decoded_refresh_token = self._auth_jwt.get_raw_jwt(refresh_token)

        if decoded_refresh_token is None or decoded_refresh_token.get("type") != TokenType.REFRESH.value:
            return [InvalidRefreshToken(message="Invalid refresh token.")]

        deleted = await self._refresh_token_data_access.delete_by_jti(jti=UUID(decoded_refresh_token["jti"]))
        if not deleted:
            return [InvalidRefreshToken(message="Invalid refresh token.")]

        return []

    async def get_token_pair(self, token_input: TokenInput) -> TokenPayload:
        user = await self._user_data_access.get_by_name(token_input.name)
        errors = self._validate_user(user, token_input)

        if errors:
            return TokenPayload(token_pair=None, errors=errors)

        token_pair = await self._create_token_pair(user)
        return TokenPayload(token_pair=token_pair, errors=[])

    async def get_token_pair_by_refresh(self, user: User, refresh_token: Optional[str] = None) -> TokenPayload:
        errors = await self._revoke_refresh_token(refresh_token=refresh_token)

        if errors:
            return TokenPayload(token_pair=None, errors=errors)

        token_pair = await self._create_token_pair(user)
        return TokenPayload(token_pair=token_pair, errors=[])
