from django.contrib.auth import get_user_model
from django.db.models import F
from django.db.models.signals import post_save
from django.dispatch import receiver

from packages.models import PackageSelfManagement

User = get_user_model()


@receiver(post_save, sender=PackageSelfManagement)
def calculate_and_save_commission(sender, instance, created, **kwargs):
    if created:
        referred_user = User.objects.get(referral_code=instance.referral_code)

        package_count = PackageSelfManagement.objects.filter(
            referral_code=referred_user.referral_code
        ).count()

        commission_values = [0.25, 0.25, 1.0]
        cycle_index = (package_count - 1) % 3

        commission_amount = instance.value * commission_values[cycle_index]
