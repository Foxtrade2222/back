import io
import string

from django.contrib.auth import get_user_model
from django.http import FileResponse
from django.urls import reverse
from django.utils.decorators import method_decorator
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics, permissions, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.test import APIClient
from rest_framework.views import APIView

from courses.models import Course, CourseApprove, Payment, SeenTopic
from courses.pdf import render_to_pdf
from courses.serializers import (
    CategorySerializer,
    CourseApproveSerializer,
    CourseSerializer,
    CreateCategorySerializer,
    CreateUpdateCourseSerializer,
    CreateUpdateModuleSerializer,
    CreateUpdateQuizSerializer,
    CreateUpdateTopicSerializer,
    ModuleSerializer,
    PublicCreateUpdateCourseSerializer,
    QuizSerializer,
    SeenTopicSerializer,
    SeenTopicsSerializer,
    SimpleTopicSerializer,
    TopicSerializer,
)
from utils.permissions import IsAdminOrTeacherUser, IsAdminUser

User = get_user_model()

# ***************************** Categories


# Create your views here.
@method_decorator(swagger_auto_schema(tags=["Category"]), name="post")
class CreateCategoryView(generics.CreateAPIView):
    serializer_class = CreateCategorySerializer
    permission_classes = [IsAdminUser]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


@method_decorator(swagger_auto_schema(tags=["Category"]), name="delete")
class DeleteCategoryView(generics.DestroyAPIView):
    serializer_class = CategorySerializer
    permission_classes = [IsAdminUser]

    def get_queryset(self):
        queryset = self.get_serializer_class().Meta.model.objects.filter()
        return queryset


@method_decorator(swagger_auto_schema(tags=["Category"]), name="get")
class RetrieveCategoryView(generics.RetrieveAPIView):
    serializer_class = CategorySerializer

    def get_queryset(self):
        queryset = self.get_serializer_class().Meta.model.objects.filter()
        return queryset


@method_decorator(swagger_auto_schema(tags=["Category"]), name="patch")
@method_decorator(swagger_auto_schema(tags=["Category"]), name="put")
class UpdateCategoryView(generics.UpdateAPIView):
    serializer_class = CategorySerializer
    permission_classes = [IsAdminUser]
    queryset = serializer_class.Meta.model.objects.all()


@method_decorator(swagger_auto_schema(tags=["Category"]), name="get")
class ListCategoryView(generics.ListAPIView):
    serializer_class = CategorySerializer
    queryset = CategorySerializer.Meta.model.objects.all()


# ***************************** Courses


@method_decorator(swagger_auto_schema(tags=["Course"]), name="post")
class CreateCourseView(generics.CreateAPIView):
    serializer_class = PublicCreateUpdateCourseSerializer
    permission_classes = [IsAdminOrTeacherUser]

    def create(self, request, *args, **kwargs):
        request.data["teacher"] = request.user.id
        request.data["slug"] = request.data.get("title")
        serializer = CreateUpdateCourseSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


@method_decorator(swagger_auto_schema(tags=["Course"]), name="patch")
@method_decorator(swagger_auto_schema(tags=["Course"]), name="put")
class UpdateCourseView(generics.UpdateAPIView):
    serializer_class = PublicCreateUpdateCourseSerializer
    permission_classes = [IsAdminOrTeacherUser]

    def get_queryset(self):
        queryset = self.get_serializer_class().Meta.model.objects.filter(
            id=self.kwargs.get("pk", None),
            teacher_id=self.request.user.id,
        )
        return queryset


@method_decorator(swagger_auto_schema(tags=["Course"]), name="get")
class RetrieveCourseView(generics.RetrieveAPIView):
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated]

    # TODO: QUE locura es estaaaaa
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)

        topics_seens = SeenTopic.objects.filter(
            student_id=self.request.user.id
        ).values_list("topic_id", flat=True)
        list_topics_seens = list(topics_seens)
        for modules in serializer.data["modules"]:
            for topic in modules["topics"]:
                if topic["id"] in list_topics_seens:
                    topic["seen"] = True
        return Response(serializer.data)

    def get_queryset(self):
        user = self.request.user
        return self.get_serializer_class().Meta.model.objects.filter(
            id=self.kwargs.get("pk", None),
        )
        if user.rol == "admin":
            return (
                self.get_serializer_class()
                .Meta.model.objects.filter(id=self.kwargs.get("pk", None))
                .prefetch_related("modules")
            )
        if user.rol == "teacher":
            return (
                self.get_serializer_class()
                .Meta.model.objects.filter(
                    teacher_id=user.id,
                    id=self.kwargs.get("pk", None),
                )
                .prefetch_related("modules")
            )
        queryset = (
            self.get_serializer_class()
            .Meta.model.objects.filter(
                students__id=user.id,
                id=self.kwargs.get("pk", None),
            )
            .prefetch_related("modules")
        )

        return queryset


@method_decorator(swagger_auto_schema(tags=["Course"]), name="delete")
class DeleteCourseView(generics.DestroyAPIView):
    serializer_class = CourseSerializer
    permission_classes = [IsAdminOrTeacherUser]

    def get_queryset(self):
        user = self.request.user
        if user.rol == "admin":
            return self.get_serializer_class().Meta.model.objects.filter(
                id=self.kwargs.get("pk", None)
            )
        queryset = self.get_serializer_class().Meta.model.objects.filter(
            id=self.kwargs.get("pk", None),
            teacher_id=user.id,
        )
        return queryset


@method_decorator(swagger_auto_schema(tags=["Course"]), name="get")
class ListCoursesView(generics.ListAPIView):
    serializer_class = CourseSerializer

    def get_queryset(self):
        queryset = self.get_serializer_class().Meta.model.objects.filter(is_active=True)
        return queryset


@method_decorator(swagger_auto_schema(tags=["Course"]), name="get")
class ListMyCoursesView(generics.ListAPIView):
    serializer_class = CourseSerializer
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request, *args, **kwargs):
        user = request.user

        data_to_response = {
            "my_courses_created": None,
            "my_enrolled_courses": None,
            "all": None,
        }

        teacher_qs = self.get_serializer_class().Meta.model.objects.filter(
            teacher_id=user.id
        )

        if teacher_qs:
            data_to_response.update(
                {"my_courses_created": self.get_serializer(teacher_qs, many=True).data}
            )

        studen_qs = self.get_serializer_class().Meta.model.objects.filter(
            students__id=user.id
        )

        if studen_qs:
            data_to_response.update(
                {"my_enrolled_courses": self.get_serializer(studen_qs, many=True).data}
            )

        if user.rol == "admin":
            data_to_response.update(
                {
                    "all": self.get_serializer(
                        self.get_serializer_class().Meta.model.objects.all(), many=True
                    ).data,
                }
            )

        return Response(data_to_response)


@method_decorator(swagger_auto_schema(tags=["Course"]), name="get")
class CertificateApproveView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None, course_id=None):
        user = self.request.user
        approve = CourseApprove.objects.filter(
            course_id=course_id, student_id=user.id
        ).first()
        course = Course.objects.get(pk=approve.course_id)

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
            "approved_id": approve.id,
        }

        pdf = render_to_pdf(data["template"], data)
        binary_io = io.BytesIO(pdf)
        response = FileResponse(binary_io)
        response["Content-Type"] = "application/octet-stream"
        response["Content-Disposition"] = 'attachment; filename="certificado.pdf"'

        return response


@method_decorator(swagger_auto_schema(tags=["Course"]), name="post")
class CourseApproveView(generics.CreateAPIView):
    serializer_class = CourseApproveSerializer
    permission_classes = [IsAuthenticated]


@method_decorator(swagger_auto_schema(tags=["Course"]), name="get")
class ListMyCoursesApproveView(generics.ListAPIView):
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        # page = self.paginate_queryset(queryset)
        # if page is not None:
        #     serializer = self.get_serializer(page, many=True)
        #     return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)

        for index, value in enumerate(serializer.data):
            approve = CourseApprove.objects.filter(
                course_id=value["id"], student_id=self.request.user.id
            ).first()
            if approve:
                value["certificate_url"] = approve.certificate_url
                serializer.data[index] = value
        return Response(serializer.data)

    def get_queryset(self):
        courses_ids = CourseApproveSerializer.Meta.model.objects.filter(
            student_id=self.request.user.id
        ).values_list("course_id", flat=True)
        list_ids = list(courses_ids)
        queryset = self.get_serializer().Meta.model.objects.filter(
            id__in=list_ids,
        )
        return queryset


# ***************************** Courses ADMIN


@method_decorator(swagger_auto_schema(tags=["Admin"]), name="get")
class ListAdminCoursesView(generics.ListAPIView):
    serializer_class = CourseSerializer
    permission_classes = [IsAdminUser]
    queryset = serializer_class.Meta.model.objects.all()


@method_decorator(swagger_auto_schema(tags=["Admin"]), name="get")
class ListAdminMostViewedCoursesView(generics.ListAPIView):
    serializer_class = CourseSerializer
    permission_classes = [IsAdminUser]
    queryset = serializer_class.Meta.model.objects.order_by("-views")


class PaymentFull(APIView):
    def post(self, request, format=None):
        # https://www.coinpayments.net/merchant-tools-ipn#statuses
        status_transactions = request.data.get("status")

        # TODO: No se que rayos estoy haciendo
        if int(status_transactions) >= 100:
            Payment.objects.create(email=request.data["email"], body=request.data)

            user = User.objects.filter(
                username=request.data["email"],
            )
            if user:
                courses = Course.objects.all()
                for course in courses:
                    course.students.add(user.first().id)
                user.update(subscription="full")
            else:
                client = APIClient()
                admin = User.objects.get(username="admin@admin.com", is_staff=True)
                client.force_authenticate(user=admin)

                client.post(
                    reverse("users:create-user"),
                    {
                        "username": request.data["email"],
                        "first_name": request.data["first_name"],
                        "last_name": request.data["last_name"],
                        "rol": "user",
                        "email": request.data["email"],
                        "subscription": "full",
                    },
                    format="json",
                )

        return Response()


class PaymentBasic(APIView):
    def post(self, request, format=None):
        # https://www.coinpayments.net/merchant-tools-ipn#statuses
        status_transactions = request.data.get("status")

        # TODO: No se que rayos estoy haciendo
        if int(status_transactions) >= 100:
            client = APIClient()
            user = User.objects.get(username="admin@admin.com", is_staff=True)
            client.force_authenticate(user=user)

            Payment.objects.create(email=request.data["email"], body=request.data)

            client.post(
                reverse("users:create-user"),
                {
                    "username": request.data["email"],
                    "first_name": request.data["first_name"],
                    "last_name": request.data["last_name"],
                    "rol": "student",
                    "email": request.data["email"],
                    "subscription": "basic",
                    "courses_ids": [],
                },
                format="json",
            )

        return Response()


# ***************************** Modules


@method_decorator(swagger_auto_schema(tags=["Module"]), name="post")
class CreateModuleView(generics.CreateAPIView):
    serializer_class = CreateUpdateModuleSerializer
    permission_classes = [IsAdminOrTeacherUser]


@method_decorator(swagger_auto_schema(tags=["Module"]), name="delete")
class DeleteModuleView(generics.DestroyAPIView):
    serializer_class = ModuleSerializer
    permission_classes = [IsAdminOrTeacherUser]

    def get_queryset(self):
        queryset = self.get_serializer_class().Meta.model.objects.filter(
            course__teacher_id=self.request.user.id,
            id=self.kwargs.get("pk", None),
        )
        return queryset


@method_decorator(swagger_auto_schema(tags=["Module"]), name="patch")
@method_decorator(swagger_auto_schema(tags=["Module"]), name="put")
class UpdateModuleView(generics.UpdateAPIView):
    serializer_class = CreateUpdateModuleSerializer
    permission_classes = [IsAdminOrTeacherUser]

    def get_queryset(self):
        queryset = self.get_serializer_class().Meta.model.objects.filter(
            course__teacher_id=self.request.user.id,
            id=self.kwargs.get("pk", None),
        )
        return queryset


@method_decorator(swagger_auto_schema(tags=["Module"]), name="get")
class RetrieveModuleView(generics.RetrieveAPIView):
    serializer_class = ModuleSerializer

    def get_queryset(self):
        queryset = self.get_serializer_class().Meta.model.objects.filter(
            id=self.kwargs.get("pk", None),
        )
        return queryset


@method_decorator(swagger_auto_schema(tags=["Module"]), name="get")
class ListModuleView(generics.ListAPIView):
    serializer_class = ModuleSerializer

    def get_queryset(self):
        queryset = self.get_serializer_class().Meta.model.objects.filter(
            course_id=self.kwargs.get("pk", None),
        )
        return queryset


@method_decorator(swagger_auto_schema(tags=["Module"]), name="get")
class ListMyModulesView(generics.ListAPIView):
    serializer_class = ModuleSerializer
    permission_classes = [IsAdminOrTeacherUser]

    def get_queryset(self):
        queryset = self.get_serializer_class().Meta.model.objects.filter(
            course__teacher_id=self.request.user.id
        )
        return queryset


# ***************************** Topics


@method_decorator(swagger_auto_schema(tags=["Topics"]), name="post")
class CreateSeenTopicView(generics.CreateAPIView):
    serializer_class = SeenTopicSerializer
    permission_classes = [IsAuthenticated]


@method_decorator(swagger_auto_schema(tags=["Topics"]), name="post")
class CreateTopicView(generics.CreateAPIView):
    serializer_class = CreateUpdateTopicSerializer
    permission_classes = [IsAdminOrTeacherUser]


@method_decorator(swagger_auto_schema(tags=["Topics"]), name="delete")
class DeleteTopicView(generics.DestroyAPIView):
    serializer_class = TopicSerializer
    permission_classes = [IsAdminOrTeacherUser]

    def get_queryset(self):
        queryset = self.get_serializer_class().Meta.model.objects.filter(
            module__course__teacher_id=self.request.user.id,
            id=self.kwargs.get("pk", None),
        )
        return queryset


@method_decorator(swagger_auto_schema(tags=["Topics"]), name="patch")
@method_decorator(swagger_auto_schema(tags=["Topics"]), name="put")
class UpdateTopicView(generics.UpdateAPIView):
    serializer_class = CreateUpdateTopicSerializer
    permission_classes = [IsAdminOrTeacherUser]

    def get_queryset(self):
        queryset = self.get_serializer_class().Meta.model.objects.filter(
            module__course__teacher_id=self.request.user.id,
            id=self.kwargs.get("pk", None),
        )
        return queryset


@method_decorator(swagger_auto_schema(tags=["Topics"]), name="get")
class ListTopicsByModuleView(generics.ListAPIView):
    serializer_class = TopicSerializer
    permission_classes = [IsAdminOrTeacherUser]

    def get_queryset(self):
        queryset = self.get_serializer_class().Meta.model.objects.filter(
            module_id=self.kwargs.get("pk", None),
        )
        return queryset


@method_decorator(swagger_auto_schema(tags=["Topics"]), name="get")
class ListTopicView(generics.ListAPIView):
    serializer_class = TopicSerializer
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        # TODO: ZZZ Despues mejorar los queries
        result = self.get_serializer(queryset)
        all_topics = TopicSerializer.Meta.model.objects.filter(
            module__course_id=queryset.module.course_id
        )

        topic_ids = list(all_topics.values_list("id", flat=True))
        current_topic = topic_ids.index(queryset.id)
        next_id = None
        previous_id = None
        if current_topic < len(topic_ids) - 1:
            next_id = topic_ids[current_topic + 1]
        if current_topic > 0:
            previous_id = topic_ids[current_topic - 1]

        simple = SimpleTopicSerializer(all_topics, many=True).data

        return Response(
            {
                "previus": {"topicID": previous_id},
                "next": {"topicID": next_id},
                "result": result.data,
                "all": simple,
            },
        )

    def get_queryset(self):
        queryset = (
            self.get_serializer_class()
            .Meta.model.objects.filter(
                id=self.kwargs.get("pk", None),
            )
            .first()
        )
        return queryset


@method_decorator(swagger_auto_schema(tags=["Topics"]), name="get")
class ListMyTopicsView(generics.ListAPIView):
    serializer_class = TopicSerializer
    permission_classes = [IsAdminOrTeacherUser]

    def get_queryset(self):
        queryset = self.get_serializer_class().Meta.model.objects.filter(
            module__course__teacher_id=self.request.user.id
        )
        return queryset


@method_decorator(swagger_auto_schema(tags=["Topics"]), name="get")
class ListSeenTopicsView(generics.ListAPIView):
    serializer_class = SeenTopicsSerializer
    permission_classes = [IsAuthenticated]

    # TODO: Mejorar la logica despues con distinct
    def get_queryset(self):
        topics_seens = SeenTopic.objects.filter(student_id=self.request.user.id).values(
            "topic__title",
            "topic__id",
            "topic__module__course__path_preview_image",
            "topic__module__course__id",
            "topic__module__course__title",
        )

        availables = []
        topics = []

        for topic in topics_seens:
            if not topic["topic__module__course__id"] in availables:
                availables.append(topic["topic__module__course__id"])
                topics.append(
                    {
                        "id": topic["topic__id"],
                        "title": topic["topic__title"],
                        "course_id": topic["topic__module__course__id"],
                        "course_name": topic["topic__module__course__title"],
                        "path_preview_image": topic[
                            "topic__module__course__path_preview_image"
                        ],
                    }
                )
        return topics[:4]


# ***************************** Quizzes


@method_decorator(swagger_auto_schema(tags=["Quizzes"]), name="post")
class CreateQuizView(generics.CreateAPIView):
    serializer_class = CreateUpdateQuizSerializer
    permission_classes = [IsAdminOrTeacherUser]


@method_decorator(swagger_auto_schema(tags=["Quizzes"]), name="delete")
class DeleteQuizView(generics.DestroyAPIView):
    serializer_class = QuizSerializer
    permission_classes = [IsAdminOrTeacherUser]
    queryset = serializer_class.Meta.model.objects.all()


@method_decorator(swagger_auto_schema(tags=["Quizzes"]), name="patch")
@method_decorator(swagger_auto_schema(tags=["Quizzes"]), name="put")
class UpdateQuizView(generics.UpdateAPIView):
    serializer_class = QuizSerializer
    permission_classes = [IsAdminOrTeacherUser]
    queryset = serializer_class.Meta.model.objects.all()


@method_decorator(swagger_auto_schema(tags=["Quizzes"]), name="get")
class ListMyQuizzesView(generics.ListAPIView):
    serializer_class = QuizSerializer
    permission_classes = [IsAdminOrTeacherUser]

    def get_queryset(self):
        user = self.request.user

        if user.rol == "admin":
            return self.get_serializer_class().Meta.model.objects.all()

        queryset = self.get_serializer_class().Meta.model.objects.filter(
            course__teacher_id=user.id
        )
        return queryset


@method_decorator(swagger_auto_schema(tags=["Quizzes"]), name="get")
class ListQuizzesView(generics.ListAPIView):
    serializer_class = QuizSerializer

    def get_queryset(self):
        queryset = self.get_serializer_class().Meta.model.objects.filter(
            course_id=self.kwargs.get("pk", None),
        )
        return queryset
