from datetime import datetime, timedelta

import requests
from django.contrib.auth import get_user_model
from django.utils.decorators import method_decorator
from django_filters import rest_framework as filters
from drf_yasg.utils import swagger_auto_schema
from loguru import logger
from rest_framework import generics, status
from rest_framework.exceptions import APIException
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from packages.models import DemoPackage
from packages.serializers import (
    CreateDemoAccountSerializer,
    CreatePackageSelfManagementSerializer,
    CreatePackageSerializer,
    PackageAccountInfoSerializer,
    PackageDemoAccountInfoSerializer,
    PackageDemoSerializer,
    PackageSelfManagementSerializer,
    PackageSerializer,
    UpdatePackageSerializer,
)
from utils.permissions import IsAdminUser

User = get_user_model()


class GenericAPIException(APIException):
    """
    raises API exceptions with custom messages and custom status codes
    """

    status_code = status.HTTP_400_BAD_REQUEST
    default_code = "error"

    def __init__(self, detail, status_code=None):
        self.detail = detail
        if status_code is not None:
            self.status_code = status_code


# Create your views here.
@method_decorator(swagger_auto_schema(tags=["Packages"]), name="post")
class CreatePackageView(generics.CreateAPIView):
    serializer_class = CreatePackageSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.validated_data["end_date"] = datetime.utcnow() + timedelta(
            days=15,
        )
        serializer.validated_data["user_id"] = self.request.user.id
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


@method_decorator(swagger_auto_schema(tags=["Packages"]), name="get")
class ListMyPackagesView(generics.ListAPIView):
    serializer_class = PackageSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = self.get_serializer_class().Meta.model.objects.filter(
            user_id=self.request.user.id
        )
        return queryset


@method_decorator(swagger_auto_schema(tags=["Packages"]), name="get")
class RetrievePackageView(generics.RetrieveAPIView):
    serializer_class = PackageAccountInfoSerializer
    queryset = PackageAccountInfoSerializer.Meta.model.objects.all()
    permission_classes = [IsAuthenticated]


@method_decorator(swagger_auto_schema(tags=["Admin"]), name="patch")
@method_decorator(swagger_auto_schema(tags=["Admin"]), name="put")
class UpdatePackageView(generics.UpdateAPIView):
    serializer_class = UpdatePackageSerializer
    permission_classes = [IsAdminUser]

    def get_queryset(self):
        queryset = self.get_serializer_class().Meta.model.objects.filter(
            id=self.kwargs.get("pk", None),
        )
        return queryset


@method_decorator(swagger_auto_schema(tags=["Admin"]), name="get")
class ListPackagesView(generics.ListAPIView):
    queryset = PackageSerializer.Meta.model.objects.all()
    serializer_class = PackageSerializer
    permission_classes = [IsAdminUser]
    filter_backends = [filters.DjangoFilterBackend]
    filterset_fields = PackageSerializer.Meta.fields + ["user__username"]


@method_decorator(swagger_auto_schema(tags=["Packages Self Management"]), name="post")
class CreatePackageSelfManagementView(generics.CreateAPIView):
    serializer_class = CreatePackageSelfManagementSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        referral_code = serializer.validated_data.get("referral_code")
        if self.request.user.referral_code == referral_code:
            raise GenericAPIException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Lo sentimos, no es posible utilizar tu propio código como referido.",
            )

        code_exists = User.objects.filter(referral_code=referral_code).exists()
        if not code_exists:
            raise GenericAPIException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Código de referido invalido.",
            )

        serializer.validated_data["user_id"] = self.request.user.id
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


@method_decorator(swagger_auto_schema(tags=["Packages Self Management"]), name="get")
class RetrievePackageSelfManagementView(generics.RetrieveAPIView):
    serializer_class = PackageSelfManagementSerializer
    queryset = PackageSelfManagementSerializer.Meta.model.objects.all()
    permission_classes = [IsAuthenticated]


@method_decorator(swagger_auto_schema(tags=["Packages Self Management"]), name="get")
class ListMyPackagesSelfManagementView(generics.ListAPIView):
    serializer_class = PackageSelfManagementSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = self.get_serializer_class().Meta.model.objects.filter(
            user_id=self.request.user.id
        )
        return queryset


@method_decorator(swagger_auto_schema(tags=["Admin"]), name="get")
class ListPackagesSelfManagementView(generics.ListAPIView):
    queryset = PackageSelfManagementSerializer.Meta.model.objects.all()
    serializer_class = PackageSelfManagementSerializer
    permission_classes = [IsAdminUser]
    filter_backends = [filters.DjangoFilterBackend]
    filterset_fields = [
        "id",
        "package_type",
        "value",
        "first_name",
        "last_name",
        "email",
        "phone_number",
        "city",
        "country",
        "postal_code",
        "tos",
        "cancellation_policies",
        "status",
        "referral_code",
        "created_at",
        "user__username",
    ]


@method_decorator(swagger_auto_schema(tags=["Packages Demo"]), name="post")
class CreateDemoPackageView(generics.CreateAPIView):
    serializer_class = CreateDemoAccountSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            value_balance = {
                "fifty_thousand": "50000",
                "one_hundred_thousand": "100000",
                "two_hundred_thousand": "200000",
                "five_hundred_thousand": "500000",
            }

            response = requests.post(
                "https://d32f-109-205-61-126.ngrok-free.app/demo-account",
                headers={
                    "token": "6tUChM3PTU0frfPPs4RzSscQrVU",
                },
                json={
                    "first_name": request.user.first_name,
                    "last_name": request.user.last_name,
                    "email": request.user.username,
                    "phone": request.user.phone_number,
                    "balance": value_balance[serializer.data.get("balance")],
                },
            )
            response.raise_for_status()

            body = response.json()

            demo = DemoPackage.objects.create(
                mt_server="EUROSTREETCapital-Server",
                mt_balance=serializer.data.get("balance"),
                mt_leverage=100,
                mt_login=body["login"],
                mt_password=body["password"],
                mt_password_investor=body["password_investor"],
                user=request.user,
            )
        except Exception as err:
            logger.exception(err)
            raise
        output_serializer = PackageDemoSerializer(demo)
        return Response(output_serializer.data, status=status.HTTP_201_CREATED)


@method_decorator(swagger_auto_schema(tags=["Packages Demo"]), name="get")
class RetrievePackageDemoView(generics.RetrieveAPIView):
    serializer_class = PackageDemoAccountInfoSerializer
    queryset = PackageDemoAccountInfoSerializer.Meta.model.objects.all()
    permission_classes = [IsAuthenticated]


@method_decorator(swagger_auto_schema(tags=["Packages Demo"]), name="get")
class ListMyPackagesDemoView(generics.ListAPIView):
    serializer_class = PackageDemoSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = self.get_serializer_class().Meta.model.objects.filter(
            user_id=self.request.user.id,
        )
        return queryset
