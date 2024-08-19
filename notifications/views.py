from django.utils.decorators import method_decorator
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from notifications.serializers import (
    NotificationSerializer,
    UpdateNotificationSerializer,
)


# Create your views here.
@method_decorator(swagger_auto_schema(tags=["Notification"]), name="get")
class ListMyNotificationsView(generics.ListAPIView):
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.rol == "user":
            queryset = (
                self.get_serializer_class()
                .Meta.model.objects.filter(
                    student_id=user.id,
                )
                .order_by("-id")[:10]
            )
        else:
            queryset = (
                self.get_serializer_class()
                .Meta.model.objects.filter(
                    teacher_id=user.id,
                )
                .order_by("-id")[:10]
            )
        return queryset


@method_decorator(swagger_auto_schema(tags=["Notification"]), name="patch")
@method_decorator(swagger_auto_schema(tags=["Notification"]), name="put")
class UpdateNotificationView(generics.UpdateAPIView):
    serializer_class = UpdateNotificationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.get_serializer_class().Meta.model.objects.filter(
            body__topic_author_id=self.request.user.id
        )
