from logging import Logger

from .auth_service import JwtToken
from .hashing_service import AbstractHashingService
from custom_exceptions import InvalidCredentialsException, AccountNotActivatedException
from models import UserDb, UserIn, UserLogin
from repositories import UserRepository
from utils import auto_repr, random_sleep

__all__ = ("UserService", )


@auto_repr(hide="jwt_token")
class UserService:
    def __init__(
            self, *,
            hashing_service: AbstractHashingService,
            jwt_token: JwtToken,
            repository: UserRepository,
            logger: Logger
    ):
        self.hashing_service = hashing_service
        self.jwt_token = jwt_token
        self.repository: UserRepository = repository
        self.logger = logger

    async def register_user(self, user: UserIn) -> str:
        hashed_password = self.hashing_service.hash(user.password)
        user.password = hashed_password
        user_db = UserDb.from_orm(user)
        activation_link = await self.repository.register_user(user_db)
        return activation_link

    async def activate_user(self, activation_token: str) -> dict[str, str]:
        return await self.repository.activate_user(activation_token)

    @random_sleep # just to make timing attack little bit harder xD
    async def login_user(self, *, user: UserLogin, refresh_token_in: str | None) -> tuple[str, str | None]:
        """
        If user exists and provides valid credentials:
            - return access and refresh tokens.

        If a hash of refresh token couldn't be saved to DB:
            - return "None" instead of refresh token and long living non-secure access token

        Refresh token is rotated if provided as an argument
        """

        # USER DOES NOT EXIST/INVALID CREDENTIALS
        if (user_db := await self._get_user_from_db(user)) is None:
            raise InvalidCredentialsException

        if not self._login_approved(user, user_db, exception_if_password_mismatch=InvalidCredentialsException):
            raise InvalidCredentialsException
        
        # CREATE/ROTATE REFRESH TOKEN
        try:
            if refresh_token_in is None:
                refresh_token = await self.jwt_token.create_refresh_token(role=user_db.role, user_id=user_db.id)
            else:
                refresh_token = await self.jwt_token.rotate_refresh_token(encoded_refresh_token=refresh_token_in)

        # RETURN LONG LIVING ACCESS TOKEN IF CREATE/ROTATE REFRESH TOKEN RAISES ERROR
        except Exception as exc:
            self.logger.error(f"Could not store refresh token (user: {user.email}, refresh_token_in: {refresh_token_in}). Error: {exc}")
            access_token = self.jwt_token.access_token_backup(role=user_db.role, id=user_db.id)
            refresh_token = None
    
        else:
            access_token = self.jwt_token.access_token_from_login(role=user_db.role, id=user_db.id)
        
        return access_token, refresh_token

    # TODO:
    async def logout_user(self):
        """"""

    # TODO:
    async def reset_password(self):
        """""" 

    # ↓↓↓ HELPER METHODS ↓↓↓ 
    async def _get_user_from_db(self, user: UserLogin) -> UserDb:
        if user.name is not None:
            field = UserDb.name == user.name
        else:
            field = UserDb.email == user.email

        user_db = await self.repository.read_resource(UserDb, filter_=field, method="one_or_none")
        return user_db

    def _login_approved(self, user_in: UserLogin, user_db: UserDb, *, exception_if_password_mismatch) -> bool:

        # TODO: what if account is not activated and activation token is expired?
        if not user_db.is_activated:
            raise AccountNotActivatedException

        password_match = self.hashing_service.verify(user_in.password, user_db.password)

        if not password_match:
            raise exception_if_password_mismatch
        else:
            return True
