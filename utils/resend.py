import os
import resend
from django.template.loader import render_to_string

resend.api_key = os.getenv("RESEND_API", "re_UxMS3V86_3kRtJ11b7xwth3h5LJr1kXvA")

EMAIL_FROM = "latam@foxtrade.capital"

def send_welcome_email(*, email, first_name, password):
    template = render_to_string(
        "bienvenidoUsuario.html",
        {
            "first_name": first_name,
            "password": password,
        },
    )
    resend.Emails.send(
        {
            "from": EMAIL_FROM,
            "to": email,
            "subject": "Bienvenido a Fox Trade Capital",
            "html": template,
        }
    )


def send_reset_password(*, email, first_name, password):
    template = render_to_string(
        "recuperar-contrasena-ultra.html",
        {
            "first_name": first_name,
            "password": password,
        },
    )
    resend.Emails.send(
        {
            "from": EMAIL_FROM,
            "to": email,
            "subject": "Recupera tu contraseña",
            "html": template,
        }
    )


def send_admin_notification(
    *,
    first_name,
    email_user,
):
    template = render_to_string(
        "avisoCorreoAdmin.html",
        {
            "first_name": first_name,
            "email_user": email_user,
        },
    )
    resend.Emails.send(
        {
            "from": EMAIL_FROM,
            "to": "ultramarkets0@gmail.com",
            "subject": "Usuario Nuevo",
            "html": template,
        }
    )
