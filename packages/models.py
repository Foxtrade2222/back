from django.conf import settings
from django.db import models

from users.fields import LowerCaseEmailField


# Create your models here.
class Package(models.Model):
    EUR = "eur"
    USD = "usd"
    CURRENCIES_CHOICES = [
        (EUR, "EUR"),
        (USD, "USD"),
    ]
    currencies = models.CharField(
        max_length=3,
        choices=CURRENCIES_CHOICES,
        default=EUR,
    )

    FIFTY_THOUSAND = "fifty_thousand"  # 299
    ONE_HUNDRED_THOUSAND = "one_hundred_thousand"  # 499
    TWO_HUNDRED_THOUSAND = "two_hundred_thousand"  # 979
    FIVE_HUNDRED_THOUSAND = "five_hundred_thousand"  # 2149
    BALANCE_CHOIES = [
        (FIFTY_THOUSAND, "FIFTY_THOUSAND"),
        (ONE_HUNDRED_THOUSAND, "ONE_HUNDRED_THOUSAND"),
        (TWO_HUNDRED_THOUSAND, "TWO_HUNDRED_THOUSAND"),
        (FIVE_HUNDRED_THOUSAND, "FIVE_HUNDRED_THOUSAND"),
    ]
    balance = models.CharField(
        max_length=30,
        choices=BALANCE_CHOIES,
        default=FIFTY_THOUSAND,
    )

    EURO_STREET_BASIC = "euro_street_basic"
    EURO_STREET_FULL = "euro_street_full"
    ACCOUNT_TYPE_CHOICES = [
        (EURO_STREET_BASIC, "EuroStreet Basic"),
        (EURO_STREET_FULL, "EuroStreet Full"),
    ]
    account_type = models.CharField(
        max_length=20,
        choices=ACCOUNT_TYPE_CHOICES,
        default=EURO_STREET_BASIC,
    )
    PENDING = "pending"
    CLOSED = "closed"
    ACTIVE = "active"
    STATUS_CHOICES = [
        (PENDING, "Pending"),
        (CLOSED, "Closed"),
        (ACTIVE, "Active"),
    ]
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default=PENDING,
    )
    value = models.FloatField(
        default=0.0,
        blank=True,
    )

    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = LowerCaseEmailField()
    phone_number = models.CharField(max_length=20, blank=True)
    address = models.CharField(max_length=50, blank=True)
    city = models.CharField(max_length=100, blank=True)
    country = models.CharField(max_length=100, blank=True)
    postal_code = models.CharField(max_length=100, blank=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="packages",
    )
    tos = models.BooleanField(default=False)
    cancellation_policies = models.BooleanField(default=False)
    end_date = models.DateTimeField()

    # MT5 fields
    mt_login = models.CharField(max_length=50)
    mt_password = models.CharField(max_length=50)
    mt_password_investor = models.CharField(max_length=50)
    mt_server = models.CharField(max_length=50)
    mt_windows = models.CharField(max_length=50)
    mt_ios = models.CharField(max_length=50)
    mt_web = models.CharField(max_length=50)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"at={self.account_type} user={self.user}"

    class Meta:
        verbose_name_plural = "Packages trader"

    def save(self, *args, **kwargs):
        prices = {
            "fifty_thousand": 299.00,
            "one_hundred_thousand": 499.00,
            "two_hundred_thousand": 979.00,
            "five_hundred_thousand": 2149.00,
        }
        self.value = prices[self.balance]
        super().save(*args, **kwargs)

    class Meta:
        ordering = ["-created_at"]


class PackageSelfManagement(models.Model):
    PENDING = "pending"
    CLOSED = "closed"
    ACTIVE = "active"
    STATUS_CHOICES = [
        (PENDING, "Pending"),
        (CLOSED, "Closed"),
        (ACTIVE, "Active"),
    ]
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default=PENDING,
    )

    AG = "ag"
    PACKAGE_TYPE_CHOICES = [
        (AG, "ICEX AG"),
    ]
    package_type = models.CharField(
        max_length=2,
        choices=PACKAGE_TYPE_CHOICES,
        default=AG,
    )
    value = models.FloatField(
        default=0.0,
        blank=True,
    )

    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = LowerCaseEmailField()
    phone_number = models.CharField(max_length=20, blank=True)
    address = models.CharField(max_length=50, blank=True)
    city = models.CharField(max_length=100, blank=True)
    country = models.CharField(max_length=100, blank=True)
    postal_code = models.CharField(max_length=100, blank=True)
    tos = models.BooleanField(default=False)
    cancellation_policies = models.BooleanField(default=False)
    referral_code = models.CharField(max_length=20)

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="packages_self_management",
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"pt={self.package_type} user={self.user}"

    def save(self, *args, **kwargs):
        self.value = 310
        super().save(*args, **kwargs)

    class Meta:
        ordering = ["-created_at"]


class DemoPackage(models.Model):
    name = models.CharField(max_length=50, default="MetaTrader Web Demo")
    account_type = models.CharField(max_length=50, default="Forex USD")
    mt_server = models.CharField(max_length=50)
    mt_balance = models.CharField(max_length=50)
    mt_leverage = models.CharField(max_length=50, blank=True)
    mt_login = models.CharField(max_length=50)
    mt_password = models.CharField(max_length=50)
    mt_password_investor = models.CharField(max_length=50)
    value = models.DecimalField(
        max_digits=3,
        decimal_places=2,
        default=0.0,
    )

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="demo_package",
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.mt_login

    class Meta:
        ordering = ["-created_at"]
        verbose_name_plural = "Packages demo"
