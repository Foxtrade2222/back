import uuid

from django.conf import settings
from django.db import models

from packages.models import Package, PackageSelfManagement


# Create your models here.
class Payment(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )
    STRIPE = "stripe"
    COINPAYMENTS = "coinpayments"
    PAYMENT_CHOICES = [
        (STRIPE, "Stripe"),
        (COINPAYMENTS, "CoinPayments"),
    ]
    payment_option = models.CharField(
        max_length=20,
        choices=PAYMENT_CHOICES,
    )

    package = models.OneToOneField(
        Package,
        related_name="payments",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    package_self_management = models.OneToOneField(
        PackageSelfManagement,
        related_name="payments",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="payments",
        on_delete=models.CASCADE,
    )
    body = models.JSONField()
    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return str(self.id)
