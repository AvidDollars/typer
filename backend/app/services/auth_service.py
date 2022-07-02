import jwt
from datetime import datetime, timedelta


__all__ = ("AuthService", )


class AuthService:
    def __init__(self, *, secret: str, token_expiration: int):
        self.secret = secret
        self.token_expiration_in_hours = token_expiration

    def encode_jwt_token(self, payload: dict):
        expires_at = datetime.utcnow() + timedelta(hours=self.token_expiration_in_hours)
        payload = dict(payload, exp=expires_at)
        return jwt.encode(payload, self.secret)
