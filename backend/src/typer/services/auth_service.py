from datetime import datetime, timedelta

import jwt
from fastapi.requests import Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from ..custom_exceptions import \
    ExpiredTokenException, \
    InvalidTokenException, \
    NotAuthenticatedException, \
    NotAuthorizedException
from ..models.enums import UserRole
from ..utils import auto_repr

__all__ = (
    "JwtToken",
    "is_moderator",
    "is_admin",
    "is_master_admin",
    "required_authentication",
    "optional_authentication"
)


@auto_repr(hide="secret")
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
                raise ExpiredTokenException
            else:
                return decoded_token

        except jwt.InvalidTokenError:
            raise InvalidTokenException


class CustomHttpBearer(HTTPBearer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    async def __call__(self, request: Request) -> HTTPAuthorizationCredentials | None:
        result = await super().__call__(request)

        # auto_error is True -> authentication is optional
        # result is None -> JWT token is not provided
        if self.auto_error is False and result is None:
            return result

        # TODO -> to be rewritten...
        from ..containers import Container  # avoiding circular import
        secret = Container().config()["secret"]  # other solutions does not work :/

        try:
            payload = jwt.decode(result.credentials, secret, algorithms=["HS256"])

            # binding "user_role" and "user_id" to the request object
            request.user_role = payload.get("role", UserRole.user)
            request.user_id = payload.get("id", None)
            return result

        except jwt.ExpiredSignatureError:
            raise ExpiredTokenException

        except jwt.InvalidTokenError:
            raise InvalidTokenException


required_authentication = CustomHttpBearer(auto_error=True)
optional_authentication = CustomHttpBearer(auto_error=False)


# to be used as dependency for ensuring authorization for accessing resources
def ensure_role(*, required_role: UserRole, request: Request):

    user_role_id = getattr(request, "user_role", None)

    if user_role_id is None:
        raise NotAuthenticatedException

    if required_role > UserRole(user_role_id):
        raise NotAuthorizedException


def is_moderator(request: Request):
    return ensure_role(request=request, required_role=UserRole.moderator)


def is_admin(request: Request):
    return ensure_role(request=request, required_role=UserRole.admin)


def is_master_admin(request: Request):
    return ensure_role(request=request, required_role=UserRole.master_admin)
