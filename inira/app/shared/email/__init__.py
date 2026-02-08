# inira/app/shared/email/__init__.py

from .email_service import send_verification_email, send_password_reset_email

__all__ = ["send_verification_email", "send_password_reset_email"]
