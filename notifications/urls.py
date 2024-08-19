from django.urls import path

from notifications.views import ListMyNotificationsView, UpdateNotificationView

urlpatterns = [
    path(
        "list/my/notifications/",
        ListMyNotificationsView.as_view(),
    ),
    path(
        "update/notification/<int:pk>/",
        UpdateNotificationView.as_view(),
    ),
]
