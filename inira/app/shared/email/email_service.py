# inira/app/shared/email/email_service.py

import os
from mailersend import emails
from .templates import (
    get_verification_email_template,
    get_password_reset_email_template,
)

MAILERSEND_API_KEY = os.getenv("MAILERSEND_API_KEY")
MAILERSEND_FROM = os.getenv("MAILERSEND_FROM")


def send_email(to_email: str, subject: str, html_content: str, text_content: str):
    """
    Función genérica para enviar emails a través de MailerSend
    """

    mailer = emails.NewEmail(MAILERSEND_API_KEY)

    mail_body = {}

    mailer.set_mail_from(
        {
            "email": MAILERSEND_FROM,
            "name": "Maroa",
        },
        mail_body,
    )

    mailer.set_mail_to(
        [
            {
                "email": to_email,
            }
        ],
        mail_body,
    )

    mailer.set_subject(subject, mail_body)
    mailer.set_html_content(html_content, mail_body)
    mailer.set_plaintext_content(text_content, mail_body)

    response = mailer.send(mail_body)

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
