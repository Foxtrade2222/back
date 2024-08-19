from django.contrib import admin

from users.models import CustomUser


@admin.register(CustomUser)
class CustomerUserAdmin(admin.ModelAdmin):
    list_display = ("username", "first_name", "last_name")
    list_filter = ("referral_code",)
