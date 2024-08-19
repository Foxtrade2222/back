from django.conf import settings
from django.db import models


# Create your models here.
class Notification(models.Model):
    COMMENT = "comment"
    REPLY_COMMENT = "reply_comment"
    TYPES = [
        (COMMENT, "Comentario"),
        (REPLY_COMMENT, "Respuesta comentario"),
    ]
    type_notification = models.CharField(
        max_length=30,
        choices=TYPES,
        default=COMMENT,
    )
    student = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="comments_notifications",
        on_delete=models.CASCADE,
        null=True,
    )
    teacher = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="teacher_comments_notifications",
        on_delete=models.CASCADE,
        null=True,
    )
    body = models.JSONField()
    read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"{self.type_notification}"
