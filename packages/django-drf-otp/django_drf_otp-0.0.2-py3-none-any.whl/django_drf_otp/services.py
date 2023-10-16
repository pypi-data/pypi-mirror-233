from typing import Dict, Optional, Type

from django.contrib.auth.models import AbstractUser

from .enums import NotificationType, TokenType
from .models import VerificationToken
from .notifiers import BaseNotifier, EmailNotifier
from .settings import otp_settings
from .strategies import BaseOTPStrategy, TOTPStrategy

TOKEN_STRATEGY_MAP = {
    TokenType.TOTP: TOTPStrategy,
}
TOKEN_NOTIFIER_MAP = {
    NotificationType.EMAIL: EmailNotifier,
}


class OTPService:
    def verify_token(
        self, token: str, token_type: Optional[TokenType] = None, extra_secret_chars: Optional[str] = None
    ) -> bool:
        strategy_class = self._get_strategy_class(token_type=token_type)
        return strategy_class.verify_token(token=token, extra_secret_chars=extra_secret_chars)

    def generate_token(self, token_type: Optional[TokenType] = None, extra_secret_chars: Optional[str] = None) -> str:
        strategy_class = self._get_strategy_class(token_type=token_type)
        return strategy_class.generate_token(extra_secret_chars=extra_secret_chars)

    def notify_user(self, user: Type[AbstractUser], token: str, extra_context: Optional[Dict] = None) -> None:
        notification_type = otp_settings.DEFAULT_NOTIFICATION_TYPE
        if hasattr(user, "notification_preference"):
            notification_type = user.notification_preference.notification_type

        notifier_class = self._get_notifier_class(notification_type=notification_type)
        notifier_class.notify(email=user.email, token=token, extra_context=extra_context or {})

    def generate_and_notify_token(
        self, user: Type[AbstractUser], token_type: Optional[TokenType] = None, extra_context: Optional[Dict] = None
    ) -> VerificationToken:
        strategy_class = self._get_strategy_class(token_type=token_type)
        verification_token = strategy_class.generate_token_for_user(user=user)
        self.notify_user(user=user, token=verification_token.token, extra_context=extra_context or {})
        return verification_token

    def _get_notifier_class(self, notification_type: NotificationType) -> BaseNotifier:
        if notification_type not in TOKEN_NOTIFIER_MAP:
            raise ValueError(
                f"'{notification_type}' is not a valid notification type. Valid notification types are '{', '.join(TOKEN_NOTIFIER_MAP.keys())}'"
            )

        notifier_class = TOKEN_NOTIFIER_MAP.get(notification_type)
        return notifier_class()

    def _get_strategy_class(self, token_type: Optional[TokenType] = None) -> BaseOTPStrategy:
        if not token_type:
            token_type = otp_settings.DEFAULT_TOKEN_TYPE

        if token_type not in TOKEN_STRATEGY_MAP:
            raise ValueError(
                f"'{token_type}' is not a valid token type. Valid token types are '{', '.join(TOKEN_STRATEGY_MAP.keys())}'"
            )

        strategy_class = TOKEN_STRATEGY_MAP.get(token_type)
        return strategy_class()
