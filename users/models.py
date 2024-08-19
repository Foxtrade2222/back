from django.contrib.auth.models import AbstractUser
from django.db import models

from users.fields import LowerCaseEmailField


# Create your models here.
class CustomUser(AbstractUser):
    ADMIN = "admin"
    TEACHER = "teacher"
    USER = "user"
    ROLES = [
        (ADMIN, "Admin"),
        (TEACHER, "Teacher"),
        (USER, "User"),
    ]
    rol = models.CharField(
        max_length=10,
        choices=ROLES,
        default=USER,
    )
    NONE = "none"
    BASIC = "basic"
    FULL = "full"
    SUBSCRIPTIONS = [
        (NONE, "Ninguno"),
        (BASIC, "Basico"),
        (FULL, "Full"),
    ]
    subscription = models.CharField(
        max_length=10,
        choices=SUBSCRIPTIONS,
        default=NONE,
        blank=True,
        null=True,
    )
    identity_card = models.CharField(max_length=30, blank=True)
    phone_number = models.CharField(max_length=20, blank=True)
    image_profile = models.URLField(blank=True)
    username = LowerCaseEmailField(unique=True)
    birth_date = models.CharField(max_length=30, blank=True)
    deferred_name = models.CharField(max_length=30, blank=True)
    deferred_document_number = models.CharField(max_length=30, blank=True)
    country_code = models.CharField(max_length=6, blank=True)
    address = models.CharField(max_length=50, blank=True)
    city = models.CharField(max_length=50, blank=True)
    state = models.CharField(max_length=50, blank=True)
    country = models.CharField(max_length=10, blank=True)
    referral_code = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return self.get_username()
