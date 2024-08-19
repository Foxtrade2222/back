from django.urls import path

from comments.views import (
    CreateCommentView,
    CreateReplyCommentView,
    DeleteCommentView,
    DeleteReplyCommentView,
    ListMyQuestionsView,
    ListUnansweredView,
    UpdateCommentView,
    UpdateReplyCommentView,
)

urlpatterns = [
    path(
        "create/comment/",
        CreateCommentView.as_view(),
    ),
    path(
        "delete/comment/<int:pk>/",
        DeleteCommentView.as_view(),
    ),
    path(
        "update/comment/<int:pk>/",
        UpdateCommentView.as_view(),
    ),
    path(
        "create/reply/comment/",
        CreateReplyCommentView.as_view(),
    ),
    path(
        "delete/reply/comment/<int:pk>/",
        DeleteReplyCommentView.as_view(),
    ),
    path(
        "update/reply/comment/<int:pk>/",
        UpdateReplyCommentView.as_view(),
    ),
    path(
        "list/unanswered/comments/",
        ListUnansweredView.as_view(),
    ),
    path(
        "list/my/comments/",
        ListMyQuestionsView.as_view(),
    ),
]
