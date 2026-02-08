# inira/app/shared/email/email_service.py

import os
import requests
from .templates import (
    get_verification_email_template,
    get_password_reset_email_template,
)

MAILGUN_DOMAIN = os.getenv("MAILGUN_DOMAIN")
MAILGUN_API_KEY = os.getenv("MAILGUN_API_KEY")
MAILGUN_FROM = os.getenv("MAILGUN_FROM")


def send_email(to_email: str, subject: str, html_content: str, text_content: str):
    """
    Función genérica para enviar emails a través de Mailgun
    """
    url = f"https://api.mailgun.net/v3/{MAILGUN_DOMAIN}/messages"

    response = requests.post(
        url,
        auth=("api", MAILGUN_API_KEY),
        data={
            "from": MAILGUN_FROM,
            "to": to_email,
            "subject": subject,
            "text": text_content,
            "html": html_content,
        },
        timeout=10,
    )

    response.raise_for_status()
    return response


def send_verification_email(to_email: str, code: str):
    """
    Envía email de verificación de cuenta con código
    """
    return send_email(
        to_email=to_email,
        subject="🥾 Verifica tu correo - Maroa",
        html_content=get_verification_email_template(code),
        text_content=f"¡Bienvenido a Maroa! Tu código de verificación es: {code}. Este código expira en 10 minutos.",
    )


def send_password_reset_email(to_email: str, code: str):
    """
    Envía email de recuperación de contraseña con código
    """
    return send_email(
        to_email=to_email,
        subject="🔐 Recupera tu contraseña - Maroa",
        html_content=get_password_reset_email_template(code),
        text_content=f"Código para restablecer tu contraseña en Maroa: {code}. Este código expira en 10 minutos. Si no solicitaste este cambio, ignora este correo.",
    )
