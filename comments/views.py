from django.utils.decorators import method_decorator
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from comments.serializers import (
    CommentSerializer,
    CommentUnansweredSerializer,
    CreateCommentSerializer,
    CreateReplyCommentSerializer,
    ReplyCommentSerializer,
    UpdateCommentSerializer,
    UpdateReplyCommentSerializer,
)
from utils import permissions


# Create your views here.
@method_decorator(swagger_auto_schema(tags=["Comment"]), name="post")
class CreateCommentView(generics.CreateAPIView):
    serializer_class = CreateCommentSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        request.data["author"] = request.user.id
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


@method_decorator(swagger_auto_schema(tags=["Comment"]), name="delete")
class DeleteCommentView(generics.DestroyAPIView):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = self.get_serializer_class().Meta.model.objects.filter(
            id=self.kwargs.get("pk"),
            author_id=self.request.user.id,
        )
        return queryset


@method_decorator(swagger_auto_schema(tags=["Comment"]), name="patch")
@method_decorator(swagger_auto_schema(tags=["Comment"]), name="put")
class UpdateCommentView(generics.UpdateAPIView):
    serializer_class = UpdateCommentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = self.get_serializer_class().Meta.model.objects.filter(
            id=self.kwargs.get("pk"),
            author_id=self.request.user.id,
        )
        return queryset


@method_decorator(swagger_auto_schema(tags=["Comment"]), name="get")
class ListUnansweredView(generics.ListAPIView):
    serializer_class = CommentUnansweredSerializer
    permission_classes = [permissions.IsAdminOrTeacherUser]

    def get_queryset(self):
        queryset = self.get_serializer_class().Meta.model.objects.filter(
            answer__body__isnull=True,
            topic__module__course__teacher_id=self.request.user.id,
        )
        return queryset


@method_decorator(swagger_auto_schema(tags=["Reply"]), name="post")
class CreateReplyCommentView(generics.CreateAPIView):
    serializer_class = CreateReplyCommentSerializer
    permission_classes = [permissions.IsAdminOrTeacherUser]

    def create(self, request, *args, **kwargs):
        request.data["author"] = request.user.id
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


@method_decorator(swagger_auto_schema(tags=["Reply"]), name="delete")
class DeleteReplyCommentView(generics.DestroyAPIView):
    serializer_class = ReplyCommentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = self.get_serializer_class().Meta.model.objects.filter(
            id=self.kwargs.get("pk"),
            author_id=self.request.user.id,
        )
        return queryset


@method_decorator(swagger_auto_schema(tags=["Reply"]), name="patch")
@method_decorator(swagger_auto_schema(tags=["Reply"]), name="put")
class UpdateReplyCommentView(generics.UpdateAPIView):
    serializer_class = UpdateReplyCommentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = self.get_serializer_class().Meta.model.objects.filter(
            id=self.kwargs.get("pk"),
            author_id=self.request.user.id,
        )
        return queryset


@method_decorator(swagger_auto_schema(tags=["Reply"]), name="get")
class ListMyQuestionsView(generics.ListAPIView):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = (
            self.get_serializer_class()
            .Meta.model.objects.filter(
                author=self.request.user.id,
            )
            .order_by("-id")
        )
        return queryset
