from rest_framework import serializers

from notifications.models import Notification
from users.serializers import PublicUserSerializer


class NotificationSerializer(serializers.ModelSerializer):
    student = PublicUserSerializer()
    teacher = PublicUserSerializer()

    class Meta:
        model = Notification
        fields = "__all__"


class UpdateNotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ("read",)
