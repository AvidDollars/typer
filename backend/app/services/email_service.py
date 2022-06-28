from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from pydantic import EmailStr
from typing import Any

from abc import ABC, abstractmethod
from ..constants import EMAIL_TEMPLATE_DIR, REGISTER_TEMPLATE_FILE_NAME

__all__ = ("EmailService", "AbstractEmailService", "UserRegistrationEmailService")


class AbstractEmailService(ABC):
    def __init__(self, *, email_config):
        self.config = ConnectionConfig(
            MAIL_USERNAME=email_config["username"],
            MAIL_PASSWORD=email_config["password"],
            MAIL_FROM=email_config["mail_from"],
            MAIL_PORT=email_config["mail_port"],
            MAIL_SERVER=email_config["mail_server"],
            MAIL_TLS=email_config["mail_tls"],
            MAIL_SSL=email_config["mail_ssl"],
            USE_CREDENTIALS=email_config["use_credentials"],
            VALIDATE_CERTS=email_config["validate_certs"],
            TEMPLATE_FOLDER=EMAIL_TEMPLATE_DIR
        )

    @abstractmethod
    async def simple_send(
            self,
            *,
            subject: str,
            recipients: list[EmailStr],
            content: dict[str, Any],
            template_name: str
    ):
        ...


class EmailService(AbstractEmailService):
    async def simple_send(
            self,
            *,
            subject: str,
            recipients: list[EmailStr],
            content: dict[str, Any],
            template_name: str
    ):
        message = MessageSchema(
            subject=subject,
            recipients=recipients,
            template_body=content,
        )

        fm = FastMail(self.config)
        await fm.send_message(message, template_name=template_name)


class UserRegistrationEmailService(EmailService):

    # method signature is overridden
    async def simple_send(self, *, recipient: EmailStr):
        await super().simple_send(
            subject="user registration",
            recipients=[recipient],
            content={"title": "user", "heading": "registration"},
            template_name=REGISTER_TEMPLATE_FILE_NAME
        )
