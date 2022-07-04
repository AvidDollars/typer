from datetime import datetime, timedelta

import jwt
from fastapi import HTTPException
from fastapi.requests import Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from ..models.enums import UserRole

__all__ = ("JwtToken", "CustomHttpBearer", "is_moderator", "is_admin", "is_master_admin")


class JwtToken:
    def __init__(
            self, *,
            secret: str,
            token_expiration: int,
            jwt_algorithm: str,
    ):
        self.secret = secret
        self.token_expiration_in_hours = token_expiration
        self.jwt_algorithm = jwt_algorithm

    def encode(self, payload: dict):
        expires_at = datetime.utcnow() + timedelta(hours=self.token_expiration_in_hours)
        payload = dict(payload, exp=expires_at)
        return jwt.encode(payload, self.secret, algorithm=self.jwt_algorithm)

    def decode(self, token: str):
        try:
            decoded_token = jwt.decode(token, self.secret, algorithms=[self.jwt_algorithm])

            if decoded_token["exp"] > datetime.now():
                raise HTTPException(401, "expired token")
            else:
                return decoded_token

        except jwt.InvalidTokenError:
            raise HTTPException(401, "invalid token")


class CustomHttpBearer(HTTPBearer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    async def __call__(self, request: Request) -> HTTPAuthorizationCredentials:

        # TODO -> to be rewritten...
        from ..containers import Container  # avoiding circular import
        secret = Container().config()["secret"]  # other solutions does not work :/

        result = await super().__call__(request)

        try:
            payload = jwt.decode(result.credentials, secret, algorithms=["HS256"])

            # binding "user_role" and "user_id" to the request object
            request.user_role = payload.get("role", UserRole.user)
            request.user_id = payload.get("id", None)  # TODO: id -> UUID in database?
            return result

        except jwt.ExpiredSignatureError:
            raise HTTPException(401, "expired token")

        except jwt.InvalidTokenError:
            raise HTTPException(401, "invalid token")


# to be used as dependency for ensuring authorization for accessing resources
def ensure_role(*, required_role: UserRole, request: Request):

    if required_role > request.user_role:
        raise HTTPException(403, "not authorized")


def is_moderator(request: Request):
    return ensure_role(request=request, required_role=UserRole.moderator)


def is_admin(request: Request):
    return ensure_role(request=request, required_role=UserRole.admin)


def is_master_admin(request: Request):
    return ensure_role(request=request, required_role=UserRole.master_admin)
