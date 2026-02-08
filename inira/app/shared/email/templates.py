LOGO_URL = "https://i.postimg.cc/N9D2k9fQ/MAROA-2-0-transparente.png"


def get_email_base_template(
    title: str,
    greeting: str,
    main_content: str,
    code: str,
    code_label: str = "Tu código de verificación",
    expiration_text: str = "Este código expira en <strong style='color: #2d5016;'>10 minutos</strong>",
    show_features: bool = True,
) -> str:
    """
    Template base para emails de Maroa

    Args:
        title: Título del header (ej: "¡Bienvenido a Maroa!")
        greeting: Saludo inicial (ej: "¡Hola aventurero! 👋")
        main_content: Texto principal antes del código
        code: El código a mostrar
        code_label: Etiqueta sobre el código
        expiration_text: Texto de expiración del código
        show_features: Si mostrar la sección de características
    """

    features_section = (
        """
        <!-- Sección informativa -->
        <tr>
            <td style="background-color: #f8f9fa; padding: 30px 40px;">
                <p style="color: #666666; font-size: 14px; line-height: 1.6; margin: 0 0 15px 0;">
                    <strong style="color: #2d5016;">¿Qué te espera en Maroa?</strong>
                </p>
                <ul style="color: #666666; font-size: 14px; line-height: 1.8; margin: 0; padding-left: 20px;">
                    <li>🥾 Rutas de senderismo personalizadas</li>
                    <li>🌾 Experiencias agroturísticas auténticas</li>
                    <li>🏞️ Descubre paisajes increíbles</li>
                    <li>🤝 Conecta con la naturaleza y comunidades locales</li>
                </ul>
            </td>
        </tr>
    """
        if show_features
        else ""
    )

    return f"""
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>{title} - Maroa</title>
    </head>
    <body style="margin: 0; padding: 0; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #f5f5f0;">
        <table width="100%" cellpadding="0" cellspacing="0" style="background-color: #f5f5f0; padding: 40px 20px;">
            <tr>
                <td align="center">
                    <!-- Container principal -->
                    <table width="600" cellpadding="0" cellspacing="0" style="background-color: #ffffff; border-radius: 16px; overflow: hidden; box-shadow: 0 4px 12px rgba(0,0,0,0.1);">
                        
                        <!-- Header con degradado de naturaleza -->
                        <tr>
                            <td style="background: linear-gradient(135deg, #4a7c2c 0%, #2d5016 100%); padding: 50px 30px; text-align: center;">
                                <img src="{LOGO_URL}" alt="Maroa Logo" style="max-width: 140px; height: auto; display: block; margin: 0 auto 25px auto;">
                                <h1 style="color: #ffffff; margin: 0; font-size: 32px; font-weight: 600; text-shadow: 0 2px 4px rgba(0,0,0,0.2);">{title}</h1>
                            </td>
                        </tr>
                        
                        <!-- Contenido principal -->
                        <tr>
                            <td style="padding: 50px 40px;">
                                <p style="color: #333333; font-size: 16px; line-height: 1.6; margin: 0 0 25px 0;">
                                    {greeting}
                                </p>
                                <p style="color: #555555; font-size: 16px; line-height: 1.6; margin: 0 0 30px 0;">
                                    {main_content}
                                </p>
                                
                                <!-- Código de verificación -->
                                <table width="100%" cellpadding="0" cellspacing="0" style="margin: 30px 0;">
                                    <tr>
                                        <td align="center" style="background-color: #f8f9fa; border-radius: 12px; padding: 30px;">
                                            <p style="color: #666666; font-size: 14px; margin: 0 0 10px 0; text-transform: uppercase; letter-spacing: 1px;">
                                                {code_label}
                                            </p>
                                            <div style="background-color: #ffffff; border: 2px dashed #4a7c2c; border-radius: 8px; padding: 20px; display: inline-block;">
                                                <span style="color: #2d5016; font-size: 36px; font-weight: 700; letter-spacing: 8px; font-family: 'Courier New', monospace;">
                                                    {code}
                                                </span>
                                            </div>
                                        </td>
                                    </tr>
                                </table>
                                
                                <p style="color: #555555; font-size: 14px; line-height: 1.6; margin: 25px 0 0 0; text-align: center;">
                                    ⏱️ {expiration_text}
                                </p>
                            </td>
                        </tr>
                        
                        {features_section}
                        
                        <!-- Footer -->
                        <tr>
                            <td style="padding: 30px 40px; text-align: center; border-top: 1px solid #e0e0e0;">
                                <p style="color: #999999; font-size: 13px; line-height: 1.6; margin: 0 0 10px 0;">
                                    Si no solicitaste esta acción, puedes ignorar este correo de forma segura.
                                </p>
                                <p style="color: #999999; font-size: 12px; line-height: 1.6; margin: 0;">
                                    © 2026 Maroa. Tu compañero de aventuras naturales.
                                </p>
                            </td>
                        </tr>
                        
                    </table>
                </td>
            </tr>
        </table>
    </body>
    </html>
    """


def get_verification_email_template(code: str) -> str:
    """
    Template para email de verificación de cuenta
    """
    return get_email_base_template(
        title="¡Bienvenido a Maroa!",
        greeting="¡Hola aventurero! 👋",
        main_content="Estás a un paso de comenzar tu viaje con Maroa. Para verificar tu cuenta y explorar experiencias únicas de senderismo y agroturismo, usa el siguiente código:",
        code=code,
        code_label="Tu código de verificación",
        expiration_text="Este código expira en <strong style='color: #2d5016;'>10 minutos</strong>",
        show_features=True,
    )


def get_password_reset_email_template(code: str) -> str:
    """
    Template para email de recuperación de contraseña
    """
    return get_email_base_template(
        title="Recupera tu contraseña",
        greeting="¡Hola! 👋",
        main_content="Recibimos una solicitud para restablecer la contraseña de tu cuenta en Maroa. Si fuiste tú, usa el siguiente código para crear una nueva contraseña:",
        code=code,
        code_label="Código de recuperación",
        expiration_text="Este código expira en <strong style='color: #2d5016;'>10 minutos</strong>",
        show_features=False,
    )
