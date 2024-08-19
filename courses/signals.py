from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver

from courses.models import Course

User = get_user_model()


@receiver(post_save, sender=Course)
def save_course(sender, instance, created, **kwargs):
    if created:
        users = User.objects.filter(subscription="full")
        for user in users:
            instance.students.add(user.id)
        instance.save()
