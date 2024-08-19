from django.conf import settings
from django.core.mail import EmailMessage

from courses.pdf import render_to_pdf


def send_email(context):
    pdf = render_to_pdf(context["template"], context)
    message = EmailMessage(
        context["title"],
        "Certificado",
        settings.DEFAULT_FROM_EMAIL,
        [
            context["email"],
        ],
    )
    message.attach("certificado.pdf", pdf)
    message.send()
