# inira/app/shared/email/email_service.py

import os
from .templates import (
    get_verification_email_template,
    get_password_reset_email_template,
)

import os
from mailersend import MailerSendClient, EmailBuilder

MAILERSEND_API_KEY = os.getenv("MAILERSEND_API_KEY")
MAILERSEND_FROM = os.getenv("MAILERSEND_FROM")

ms = MailerSendClient(api_key=MAILERSEND_API_KEY)


def send_email(to_email: str, subject: str, html_content: str, text_content: str):

    email = (
        EmailBuilder()
        .from_email(MAILERSEND_FROM, "Maroa")
        .to_many([{"email": to_email}])
        .subject(subject)
        .html(html_content)
        .text(text_content)
        .build()
    )

    response = ms.emails.send(email)

    return response



def send_verification_email(to_email: str, code: str):
    return send_email(
        to_email=to_email,
        subject="🥾 Verifica tu correo - Maroa",
        html_content=get_verification_email_template(code),
        text_content=f"¡Bienvenido a Maroa! Tu código de verificación es: {code}. Este código expira en 10 minutos.",
    )


def send_password_reset_email(to_email: str, code: str):
    return send_email(
        to_email=to_email,
        subject="🔐 Recupera tu contraseña - Maroa",
        html_content=get_password_reset_email_template(code),
        text_content=f"Código para restablecer tu contraseña en Maroa: {code}. Este código expira en 10 minutos. Si no solicitaste este cambio, ignora este correo.",
    )
