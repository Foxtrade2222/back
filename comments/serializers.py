from rest_framework import serializers

from comments.models import Comment, ReplyComment
from courses.models import Topic
from users.serializers import PublicUserSerializer


class ReplyCommentSerializer(serializers.ModelSerializer):
    author = PublicUserSerializer()

    class Meta:
        model = ReplyComment
        fields = "__all__"


class CreateReplyCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReplyComment
        fields = ("author", "comment", "body")


class UpdateReplyCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReplyComment
        fields = ("body",)


class TopicSerializerComment(serializers.ModelSerializer):
    module_name = serializers.CharField(source="module.name")

    class Meta:
        model = Topic
        fields = (
            "id",
            "title",
            "module_id",
            "module_name",
            "description",
            "created_at",
            "updated_at",
        )


class CommentSerializer(serializers.ModelSerializer):
    author = PublicUserSerializer()
    answer = ReplyCommentSerializer()

    class Meta:
        model = Comment
        fields = "__all__"


class CommentUnansweredSerializer(serializers.ModelSerializer):
    author = PublicUserSerializer()
    topic = TopicSerializerComment()
    answer = ReplyCommentSerializer()

    class Meta:
        model = Comment
        fields = "__all__"


class CreateCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ("author", "topic", "body")


class UpdateCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ("body",)
