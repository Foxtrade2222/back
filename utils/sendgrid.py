from django.core.mail import EmailMessage


def send_welcome_email(*, email, first_name, password):
    msg = EmailMessage(
        from_email="support@icexlatam.com",
        to=[email],
    )
    msg.template_id = "d-c092965f4f2d494aa5c4614d4358789a"
    msg.dynamic_template_data = {
        "first_name": first_name,
        "password": password,
    }
    msg.send(fail_silently=False)


def send_reset_password(*, email, first_name, password):
    msg = EmailMessage(
        from_email="support@icexlatam.com",
        to=[email],
    )
    msg.template_id = "d-aba89779c3ac46e2936a6b8c35c9bf4c"
    msg.dynamic_template_data = {
        "first_name": first_name,
        "password": password,
    }
    msg.send(fail_silently=False)


def send_admin_notification(
    *,
    first_name,
    email_user,
    identity_card,
    phone_number,
    deferred_name,
    deferred_document_number
):
    msg = EmailMessage(
        from_email="support@icexlatam.com",
        to=["Backoffice@icexlatam.com"],
    )
    msg.template_id = "d-11f093b75aab4e1fa5f54eaca9a11c22"
    msg.dynamic_template_data = {
        "first_name": first_name,
        "email_user": email_user,
        "identity_card": identity_card,
        "phone_number": phone_number,
        "deferred_name": deferred_name,
        "deferred_document_number": deferred_document_number,
    }
    msg.send(fail_silently=False)
