from django.db.models.signals import post_save
from django.dispatch import receiver

from comments.models import Comment, ReplyComment
from notifications.models import Notification


@receiver(post_save, sender=Comment)
def save_comment(sender, instance, created, **kwargs):
    # TODO: Reducir la cantidad de consultas
    if created:
        data = {
            "type_notification": "comment",
            "student_id": instance.author.id,
            "body": {
                "comment": instance.body,
                "comment_id": instance.id,
                "comment_created_at": str(instance.created_at),
                "topic_name": instance.topic.title,
                "student_name": f"{instance.author.first_name} {instance.author.last_name}",
                "student_image_profile": instance.author.image_profile or None,
            },
        }
        Notification.objects.create(**data)


@receiver(post_save, sender=ReplyComment)
def save_reply_comment(sender, instance, created, **kwargs):
    # TODO: Reducir la cantidad de consultas
    if created:
        data = {
            "type_notification": "reply_comment",
            "student_id": instance.comment.author.id,
            "teacher_id": instance.author.id,
            "body": {
                "comment": instance.comment.body,
                "reply_comment": instance.body,
                "reply_comment_id": instance.id,
                "reply_comment_created_at": str(instance.created_at),
                "topic_name": instance.comment.topic.title,
                "student_name": f"{instance.comment.author.first_name} {instance.comment.author.last_name}",
                "student_image_profile": instance.comment.author.image_profile or None,
                "teacher_name": f"{instance.author.first_name} {instance.author.last_name}",
                "teacher_image_profile": instance.author.image_profile or None,
            },
        }
        Notification.objects.create(**data)
