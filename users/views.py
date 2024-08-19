from django.db.models import Count, Q
from django.db.models.functions import TruncMonth
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django_filters import rest_framework as filters
from drf_yasg.utils import swagger_auto_schema
from knox.models import AuthToken
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from courses.models import Course
from users.filters import UserFilter
from users.serializers import (
    AllUserSerializer,
    ChangePasswordSerializer,
    CreateUserByAdmin,
    LoginUserSerializer,
    ResetPasswordSerializer,
    SignUpUserSerializer,
    StatisticsSerializer,
    UpdateUserProfileSerializer,
    UpdateUserSerializer,
)
from utils.permissions import IsAdminUser
from django.views.generic.base import TemplateView


# Create your views here.
class HomePageView(TemplateView):
    template_name = "home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        print("HOLA")
        return context


@method_decorator(swagger_auto_schema(tags=["Auth"]), name="post")
class SignUpUserView(generics.CreateAPIView):
    serializer_class = SignUpUserSerializer

    @swagger_auto_schema(tags=["Auth"])
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(
            {"message": "Usuario registrado existosamente."},
            status=status.HTTP_201_CREATED,
        )


class LoginUserView(generics.GenericAPIView):
    serializer_class = LoginUserSerializer
    throttle_scope = "login"

    @swagger_auto_schema(tags=["Auth"])
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data
        return Response(
            {
                "user": AllUserSerializer(user).data,
                "token": AuthToken.objects.create(user)[1],
            }
        )


@method_decorator(swagger_auto_schema(tags=["Auth"]), name="post")
class ResetPasswordView(generics.CreateAPIView):
    serializer_class = ResetPasswordSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_200_OK)


@method_decorator(swagger_auto_schema(tags=["Profile"]), name="patch")
@method_decorator(swagger_auto_schema(tags=["Profile"]), name="put")
class ChangePasswordView(generics.UpdateAPIView):
    serializer_class = ChangePasswordSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        queryset = self.get_queryset()
        obj = get_object_or_404(queryset)
        self.check_object_permissions(self.request, obj)
        return obj

    def get_queryset(self):
        queryset = self.get_serializer_class().Meta.model.objects.filter(
            id=self.request.user.id,
        )
        return queryset


@method_decorator(swagger_auto_schema(tags=["Profile"]), name="get")
class RetrieveProfileView(generics.RetrieveAPIView):
    serializer_class = AllUserSerializer
    queryset = AllUserSerializer.Meta.model.objects.all()
    permission_classes = [IsAuthenticated]

    def get_object(self):
        queryset = self.get_queryset()
        obj = get_object_or_404(queryset, id=self.request.user.id)
        return obj


@method_decorator(swagger_auto_schema(tags=["Profile"]), name="patch")
@method_decorator(swagger_auto_schema(tags=["Profile"]), name="put")
class UpdateProfileView(generics.UpdateAPIView):
    serializer_class = UpdateUserProfileSerializer
    permission_classes = [IsAuthenticated]

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, "_prefetched_objects_cache", None):
            instance._prefetched_objects_cache = {}

        return Response(AllUserSerializer(instance).data)

    def get_object(self):
        queryset = self.get_queryset()
        obj = get_object_or_404(queryset)
        self.check_object_permissions(self.request, obj)
        return obj

    def get_queryset(self):
        queryset = self.get_serializer_class().Meta.model.objects.filter(
            id=self.request.user.id,
        )
        return queryset


@method_decorator(swagger_auto_schema(tags=["Admin"]), name="patch")
@method_decorator(swagger_auto_schema(tags=["Admin"]), name="put")
class EditUserView(generics.UpdateAPIView):
    serializer_class = UpdateUserSerializer
    permission_classes = [IsAdminUser]

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)

        subscription = serializer.validated_data.get("subscription").strip().lower()
        if subscription == "full" or instance.rol == "admin":
            courses = Course.objects.filter()
            for course in courses:
                course.students.add(instance.id)
        elif subscription == "basic":
            courses_ids = serializer.validated_data.get("courses_ids")
            courses = Course.objects.filter(id__in=courses_ids)
            for course in courses:
                course.students.add(instance.id)

        self.perform_update(serializer)

        if getattr(instance, "_prefetched_objects_cache", None):
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)

    def perform_update(self, serializer):
        serializer.save()

    def partial_update(self, request, *args, **kwargs):
        kwargs["partial"] = True
        return self.update(request, *args, **kwargs)

    def get_queryset(self):
        queryset = self.get_serializer_class().Meta.model.objects.filter(
            id=self.kwargs.get("pk", None)
        )
        return queryset


@method_decorator(swagger_auto_schema(tags=["Admin"]), name="post")
class CreateUserView(generics.CreateAPIView):
    serializer_class = CreateUserByAdmin
    permission_classes = [IsAdminUser]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = self.perform_create(serializer)
        # TODO: Mejorar luego con select_related
        if instance.rol == "admin":
            courses = Course.objects.filter()
            for course in courses:
                course.students.add(instance.id)
        return Response(
            AllUserSerializer(instance).data, status=status.HTTP_201_CREATED
        )

    def perform_create(self, serializer):
        return serializer.save()


@method_decorator(swagger_auto_schema(tags=["Admin"]), name="delete")
class DeleteUserView(generics.DestroyAPIView):
    serializer_class = AllUserSerializer
    permission_classes = [IsAdminUser]
    queryset = AllUserSerializer.Meta.model.objects.all()


@method_decorator(swagger_auto_schema(tags=["Admin"]), name="get")
class RetrieveUserView(generics.RetrieveAPIView):
    serializer_class = AllUserSerializer
    queryset = AllUserSerializer.Meta.model.objects.all()
    permission_classes = [IsAdminUser]


@method_decorator(swagger_auto_schema(tags=["Admin"]), name="get")
class ListTotalStudentsView(generics.ListAPIView):
    serializer_class = AllUserSerializer
    permission_classes = [IsAdminUser]

    def get_queryset(self):
        queryset = self.get_serializer_class().Meta.model.objects.filter(rol="user")
        return queryset


@method_decorator(swagger_auto_schema(tags=["Admin"]), name="get")
class ListTotalActiveStudentsView(generics.ListAPIView):
    serializer_class = AllUserSerializer
    permission_classes = [IsAdminUser]

    def get_queryset(self):
        queryset = self.get_serializer_class().Meta.model.objects.filter(
            rol="user", is_active=True
        )
        return queryset


@method_decorator(swagger_auto_schema(tags=["Admin"]), name="get")
class ListTotalTeachersView(generics.ListAPIView):
    serializer_class = AllUserSerializer
    permission_classes = [IsAdminUser]

    def get_queryset(self):
        queryset = self.get_serializer_class().Meta.model.objects.filter(rol="teacher")
        return queryset


@method_decorator(swagger_auto_schema(tags=["Admin"]), name="get")
class ListTotalAdminsView(generics.ListAPIView):
    serializer_class = AllUserSerializer
    permission_classes = [IsAdminUser]

    def get_queryset(self):
        queryset = self.get_serializer_class().Meta.model.objects.filter(rol="admin")
        return queryset


@method_decorator(swagger_auto_schema(tags=["Admin"]), name="get")
class ListStatisticsAdminsView(generics.ListAPIView):
    serializer_class = StatisticsSerializer
    permission_classes = [IsAdminUser]

    def list(self, request, *args, **kwargs):
        totals = AllUserSerializer.Meta.model.objects.aggregate(
            total_admins=Count(
                "id",
                filter=Q(rol="admin"),
            ),
            total_students=Count(
                "id",
                filter=Q(rol="user"),
            ),
            total_teachers=Count(
                "id",
                filter=Q(rol="teacher"),
            ),
            total_subscribers=Count(
                "id",
                filter=(Q(subscription="basic") | Q(subscription="full")),
            ),
        )
        users_by_month = (
            list(
                AllUserSerializer.Meta.model.objects.annotate(
                    date=TruncMonth("date_joined"),
                )
                .values("date")
                .annotate(
                    users=Count("id"),
                )
                .values("date", "users"),
            ),
        )
        return Response(
            {
                "avg_users_months": users_by_month,
                **totals,
            },
        )


@method_decorator(swagger_auto_schema(tags=["Admin"]), name="get")
class ListUsersView(generics.ListAPIView):
    queryset = AllUserSerializer.Meta.model.objects.all()
    serializer_class = AllUserSerializer
    permission_classes = [IsAdminUser]
    filter_backends = [filters.DjangoFilterBackend]
    filterset_fields = AllUserSerializer.Meta.fields
    filterset_class = UserFilter
