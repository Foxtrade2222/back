import string

from rest_framework import serializers

from comments.serializers import CommentSerializer
from courses.models import (
    Category,
    Course,
    CourseApprove,
    Module,
    Quiz,
    SeenTopic,
    Topic,
)
from users.serializers import PublicUserSerializer
from utils.email import send_email


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


class CreateCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ("name",)


class CreateUpdateCourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        exclude = (
            "created_at",
            "updated_at",
            "students",
            "slug",
            "views",
            "category",
        )


class PublicCreateUpdateCourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        exclude = (
            "created_at",
            "updated_at",
            "students",
            "slug",
            "views",
            "teacher",
            "category",
        )


class SimpleTopicSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    title = serializers.CharField()
    seen = serializers.BooleanField()


class TopicSerializer(serializers.ModelSerializer):
    course_id = serializers.CharField(source="module.course.id")
    course_name = serializers.CharField(source="module.course.title")
    course_path_preview_image = serializers.CharField(
        source="module.course.path_preview_image"
    )
    module_name = serializers.CharField(source="module.name")
    comments = CommentSerializer(many=True)

    class Meta:
        model = Topic
        fields = (
            "id",
            "title",
            "course_id",
            "course_name",
            "course_path_preview_image",
            "module_id",
            "module_name",
            "description",
            "video",
            "seen",
            "files",
            "links",
            "comments",
            "created_at",
            "updated_at",
        )


class CreateUpdateTopicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Topic
        fields = (
            "title",
            "description",
            "video",
            "module",
            "files",
            "links",
            "seen",
        )


class QuizSerializer(serializers.ModelSerializer):
    course_name = serializers.CharField(source="course.title")

    class Meta:
        model = Quiz
        fields = (
            "id",
            "course_id",
            "course_name",
            "questions",
            "created_at",
            "updated_at",
        )


class CreateUpdateQuizSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quiz
        fields = (
            "questions",
            "course",
        )


class ModuleSerializer(serializers.ModelSerializer):
    course_name = serializers.CharField(source="course.title")
    topics = TopicSerializer(many=True)

    class Meta:
        model = Module
        fields = "__all__"


class CreateUpdateModuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Module
        fields = (
            "id",
            "name",
            "course",
        )


class CourseSerializer(serializers.ModelSerializer):
    teacher = PublicUserSerializer()
    category = CategorySerializer()
    students = PublicUserSerializer(many=True)
    modules = ModuleSerializer(many=True)
    quizzes = QuizSerializer()

    class Meta:
        model = Course
        fields = "__all__"


class CourseApproveSerializer(serializers.ModelSerializer):
    course_id = serializers.PrimaryKeyRelatedField(queryset=Course.objects.all())

    class Meta:
        model = CourseApprove
        fields = ("course_id",)

    def create(self, validated_data):
        user = self.context["request"].user
        course = validated_data["course_id"]
        validated_data["course_id"] = course.id
        validated_data["student_id"] = user.id

        instance = self.Meta.model._default_manager.create(**validated_data)
        data = {
            "email": user.username,
            "template": "certificado.html",
            "title": "Aprobado",
            "first_name": string.capwords(user.first_name)
            if user.first_name != ""
            else "",
            "last_name": string.capwords(user.last_name)
            if user.first_name != ""
            else "",
            "course_name": course.title,
            "approved_id": instance.id,
        }
        send_email(data)
        return instance


class SeenTopicSerializer(serializers.ModelSerializer):
    topic = serializers.PrimaryKeyRelatedField(queryset=Topic.objects.all())

    class Meta:
        model = SeenTopic
        fields = ("topic",)

    def create(self, validated_data):
        user = self.context["request"].user
        validated_data["student_id"] = user.id
        instance = self.Meta.model._default_manager.create(**validated_data)
        return instance


class SeenTopicsSerializer(serializers.Serializer):
    id = serializers.CharField()
    title = serializers.CharField()
    course_id = serializers.CharField()
    course_name = serializers.CharField()
    path_preview_image = serializers.CharField()
