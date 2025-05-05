from datetime import datetime, timedelta, timezone
from functools import partial
from logging import Logger
from uuid import UUID

import jwt
from fastapi.requests import Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from custom_exceptions import \
    ExpiredTokenException, \
    InvalidTokenException, \
    NotAuthenticatedException, \
    NotAuthorizedException

import containers
from repositories import RefreshTokenRepository
from services.hashing_service import AbstractHashingService
from models import UserRole, RefreshTokenDb
from utils import auto_repr, CustomJSONEncoder


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
            token_expiration: float,
            safe_token_expiration: float,
            refresh_token_expiration: float,
            jwt_algorithm: str,
            hashing_service: AbstractHashingService,
            logger: Logger,
            refresh_token_repository: RefreshTokenRepository
    ):
        self.secret = secret
        self.token_expiration_in_hours = token_expiration
        self.safe_token_expiration_in_hours = safe_token_expiration
        self.refresh_token_expiration_in_hours = refresh_token_expiration
        self.jwt_algorithm = jwt_algorithm
        self.hashing_service = hashing_service
        self.logger = logger
        self.json_encoder = partial(CustomJSONEncoder, logger=logger)
        self.jwt_decoder = partial(jwt.decode, key=self.secret, algorithms=[self.jwt_algorithm])
        self.refresh_token_repository = refresh_token_repository

    def access_token_from_login(self, *, role: str, id: str) -> str:
        """
        To be used for 'login' action. Generates 'secure' token, which can be used for sensitive operations.
        'Sensitive operation' could be performed within 'secureUntil' time window.
        """
        return self._encode({"role": role, "id": id, "token_type": "access"}, is_secure=True)
    
    def access_token_backup(self, *, role: str, id: str) -> str:
        """ 
        If e.g. saving refresh token to DB fails.
        Access token will be long living, but couldn't be used for safe actions.
        """
        return self._encode({"role": role, "id": id, "token_type": "access"}, is_secure=False, expiration_in_hours=4)
    
    async def create_token_pair_from_refresh(self, *, encoded_refresh_token: str) -> tuple[str, str | None]:
        """ Creates new access token from refresh token + rotates refresh token. """
        access_token = await self.access_token_from_refresh(encoded_refresh_token=encoded_refresh_token) 
        refresh_token = await self.rotate_refresh_token(encoded_refresh_token=encoded_refresh_token)
        return access_token, refresh_token

    async def access_token_from_refresh(self, *, encoded_refresh_token: str) -> str:
        """ Returns unsafe access token if refresh token is valid. """

        try:
            decoded_token: dict = self.jwt_decoder(encoded_refresh_token)

        except jwt.PyJWTError as error:
            self.logger.error(f"Refresh token cannot be decoded (token: {encoded_refresh_token}). Error: {error}")
            encoded_refresh_token_hash = self.hashing_service.hash(encoded_refresh_token)
            rows_affected = await self.refresh_token_repository.delete_refresh_token(refresh_token_hash=encoded_refresh_token_hash)
            
            if rows_affected == 0:
                self.logger.warning(f"Refresh token was not deleted from the DB (token={encoded_refresh_token})")
            raise NotAuthorizedException

        else:
            role: str = decoded_token["role"]
            user_id: UUID = decoded_token["id"]

            return self._encode(
                {"role": role, "id": user_id},
                is_secure=False,
                expiration_in_hours=self.token_expiration_in_hours
            )

    async def rotate_refresh_token(self, *, encoded_refresh_token: str) -> str:
        """
        Deletes provided refresh token and creates a new one.
        Returns "None" if a new refresh token cannot be crated.
        """
        
        encoded_refresh_token_hash = self.hashing_service.hash(encoded_refresh_token)

        # DELETE OLD REFRESH TOKEN
        try:
            rows_affected = await self.refresh_token_repository.delete_refresh_token(refresh_token_hash=encoded_refresh_token_hash)
            
            if rows_affected == 0:
                self.logger.warning(f"Refresh token was not deleted from the DB (token={encoded_refresh_token})")

        except Exception as exc:
            self.logger.error(f"Error when trying to delete old refresh token (token={encoded_refresh_token}): {exc}")

        # CREATE NEW REFRESH TOKEN
        try:
            decoded_token: dict = self.jwt_decoder(encoded_refresh_token)
            role: str = decoded_token["role"]
            user_id: str = decoded_token["id"]
            new_refresh_token = await self.create_refresh_token(role=role, user_id=user_id)

        except jwt.PyJWTError as error:
            self.logger.error(f"Cannot create new refresh token (token={encoded_refresh_token}). Error: {error}")
            raise NotAuthorizedException

        else:
            return new_refresh_token

    async def create_refresh_token(self, *, role: str, user_id: str | None) -> str | None:
        encoded_token = self._encode(
            {"role": role, "id": user_id, "token_type": "refresh"},
            expiration_in_hours=self.refresh_token_expiration_in_hours,
        )

        refresh_token_db = {
            "refresh_token_hash": self.hashing_service.hash(encoded_token),
            "user_id": user_id,
            "expires_in": self._create_expiration_timestamp_db(hours=self.refresh_token_expiration_in_hours),
        }

        refresh_token_hash = RefreshTokenDb(**refresh_token_db) 
        message_on_error = f"Token '{encoded_token}' was not saved to DB."

        try:   
            rows_affected = await self.refresh_token_repository.store_refresh_token(refresh_token_hash=refresh_token_hash)

            if rows_affected == 0:
                self.logger.error(message_on_error)
                return None

        except Exception as error:
            self.logger.error(f"{message_on_error} Error: {error}")
            return None

        return encoded_token

    def _create_expiration_timestamp_db(self, *, hours: float):
        """ Creates expiration timestamp for DB usage. """
        dt_now = datetime.now()
        expiration = dt_now + timedelta(hours=hours)
        return expiration
        
    # todo: use "_crate_expiratin_timestamp"
    def _encode(self, payload: dict, *, is_secure = False, expiration_in_hours = None):
        dt_now = datetime.now(timezone.utc)
        expiration = expiration_in_hours if expiration_in_hours is not None else self.token_expiration_in_hours
        expires_at = dt_now + timedelta(hours=expiration)
        secure_until = dt_now + timedelta(hours=self.safe_token_expiration_in_hours) if is_secure else datetime.fromtimestamp(0)
        payload = dict(payload, exp=expires_at, isSecure=is_secure, secureUntil=int(secure_until.timestamp()))
        return jwt.encode(payload, self.secret, algorithm=self.jwt_algorithm, json_encoder=self.json_encoder)


# TODO: inject logger... "partial(CustomHttpBearer, logger=logger)"
# TODO: inject "JwtToken" service for manipulation with jwt tokens
class CustomHttpBearer(HTTPBearer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    async def __call__(self, request: Request) -> HTTPAuthorizationCredentials | None:
        result = await super().__call__(request)

        # auto_error is True -> authentication is optional
        # result is None -> JWT token is not provided
        if self.auto_error is False and result is None:
            return result

        secret = containers.Container().config()["secret"]

        try:
            # TODO: inject "JwtToken" and use its decoder
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


# TODO: cannot inject logger (circular imports)... create Service to be declared in the container?
# to be used as dependency for ensuring authorization for accessing resources
def ensure_role(*, required_role: UserRole, request: Request):

    user_role_id = getattr(request, "user_role", None)

    if user_role_id is None:
        raise NotAuthenticatedException

    if required_role > UserRole(user_role_id):
        # TODO: logging
        raise NotAuthorizedException


def is_moderator(request: Request):
    return ensure_role(request=request, required_role=UserRole.moderator)


def is_admin(request: Request):
    return ensure_role(request=request, required_role=UserRole.admin)


def is_master_admin(request: Request):
    return ensure_role(request=request, required_role=UserRole.master_admin)
