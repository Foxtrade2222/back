from django.conf import settings
from django.db import models

from courses.models import Topic


# Create your models here.
class Comment(models.Model):
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name="comments", on_delete=models.CASCADE
    )
    topic = models.ForeignKey(
        Topic,
        related_name="comments",
        on_delete=models.CASCADE,
    )
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.body


class ReplyComment(models.Model):
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name="answers", on_delete=models.CASCADE
    )
    comment = models.OneToOneField(
        Comment,
        related_name="answer",
        on_delete=models.CASCADE,
    )
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.body
