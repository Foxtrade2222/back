from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

User = get_user_model()


class Command(BaseCommand):
    help = "Displays current time"

    def handle(self, *args, **kwargs):
        try:
            user = User.objects.get(username="admin@admin.com")
            print(f"User already exist: {user}")
        except User.DoesNotExist:
            user = User.objects.create_superuser(
                username="admin@admin.com",
                email="admin@admin.com",
                password="PGkqFj_AQH7O1X4FETDRI4t5ykEPgJJySAVCjaoM5CQ",
                rol="admin",
                is_staff=True,
            )
            print(f"User created: {user}")
