from django.urls import reverse
from django.utils.decorators import method_decorator
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics, status
from rest_framework.exceptions import APIException
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from courses.models import Course
from packages.models import Package, PackageSelfManagement
from payments import coinpayment_api, stripe
from payments.models import Payment
from payments.serializers import (
    CreatePaymentPackageCoinpaymentSerializer,
    CreatePaymentPackageSelfManagementCoinpaymentSerializer,
    CreatePaymentPackageSelfManagementStripeSerializer,
    CreatePaymentPackageStripeSerializer,
    PaymentPackageStripeSerializer,
)


# Create your views here.
@method_decorator(swagger_auto_schema(tags=["Packages"]), name="post")
class CreatePaymentPackageStripeView(generics.CreateAPIView):
    serializer_class = CreatePaymentPackageStripeSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            package = Package.objects.get(
                id=serializer.data.get("package_id"),
            )
            response_stripe = stripe.Charge.create(
                amount=int(package.value * 100),
                currency="usd",
                source=serializer.data.get("token_id"),
                description="Paquete de programas de financiación ICEX",
            )
            if response_stripe["status"] == "succeeded":
                Payment.objects.create(
                    payment_option="stripe",
                    user_id=request.user.id,
                    body=response_stripe,
                    amount=package.value,
                    package=package,
                )
                package.status = "active"
                package.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(
                {"detail": "transaction failed"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        except Exception as e:
            raise APIException(str(e))


@method_decorator(swagger_auto_schema(tags=["Packages"]), name="post")
class CreatePaymentPackageCoinpaymentView(generics.CreateAPIView):
    serializer_class = CreatePaymentPackageCoinpaymentSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            package = Package.objects.get(
                id=serializer.data.get("package_id"),
            )
            transaction = coinpayment_api.create_transaction(
                amount=package.value,
                currency1="USD",
                currency2=serializer.data.get("currency2"),
                buyer_email=request.user.username,
                ipn_url=request.build_absolute_uri(
                    reverse(
                        "payments:ipn_package",
                        args=(serializer.data.get("package_id"),),
                    ),
                ),
            )
            if transaction["error"] != "ok":
                print(transaction)
                return Response(
                    {"detail": "transaction failed"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            return Response(
                transaction["result"],
                status=status.HTTP_201_CREATED,
            )
        except Exception as e:
            raise APIException(str(e))


class IPNPackageCoinpaymentView(APIView):
    def post(self, request, package_id=None, format=None):
        status_transactions = request.data.get("status")

        if int(status_transactions) >= 100:
            package = Package.objects.get(id=package_id)
            package.status = "active"
            package.save()

            Payment.objects.create(
                payment_option="coinpayments",
                user_id=package.user.id,
                body=request.data,
                amount=request.data.get("amount2"),
                package=package,
            )
        return Response()


@method_decorator(swagger_auto_schema(tags=["Packages Self Management"]), name="post")
class CreatePaymentPackageSelfManagementStripeView(generics.CreateAPIView):
    serializer_class = CreatePaymentPackageSelfManagementStripeSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            token_id = serializer.validated_data.get("token_id")
            package = PackageSelfManagement.objects.get(
                id=serializer.validated_data.get("package_self_management_id"),
            )

            response_stripe = stripe.Charge.create(
                amount=int(package.value * 100),
                currency="usd",
                source=token_id,
                description="Autogestión ICEX",
            )

            if response_stripe["status"] == "succeeded":
                Payment.objects.create(
                    payment_option="stripe",
                    user_id=request.user.id,
                    body=response_stripe,
                    amount=package.value,
                    package_self_management=package,
                )

                courses = Course.objects.all()
                for course in courses:
                    course.students.add(request.user.id)

                package.status = "active"
                package.save()

                package.user.subscription = "full"
                package.user.save()

                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(
                {"detail": "transaction failed"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        except Exception as e:
            raise APIException(str(e))


@method_decorator(swagger_auto_schema(tags=["Packages Self Management"]), name="post")
class CreatePaymentPackageSelfManagementCoinpaymentView(generics.CreateAPIView):
    serializer_class = CreatePaymentPackageSelfManagementCoinpaymentSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            package = PackageSelfManagement.objects.get(
                id=serializer.validated_data.get("package_self_management_id"),
            )
            transaction = coinpayment_api.create_transaction(
                amount=package.value,
                currency1="USD",
                currency2=serializer.data.get("currency2"),
                buyer_email=request.user.username,
                ipn_url=request.build_absolute_uri(
                    reverse(
                        "payments:ipn_package_self_management",
                        args=(serializer.data.get("package_self_management_id"),),
                    ),
                ),
            )

            if transaction["error"] != "ok":
                return Response(
                    {"detail": f"transaction failed {transaction}"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            return Response(
                transaction["result"],
                status=status.HTTP_201_CREATED,
            )
        except Exception as e:
            raise APIException(str(e))


class IPNSelfManagementPackageCoinpaymentView(APIView):
    def post(self, request, package_id=None, format=None):
        status_transactions = request.data.get("status")

        if int(status_transactions) >= 100:
            package = PackageSelfManagement.objects.get(id=package_id)

            Payment.objects.create(
                payment_option="coinpayments",
                user_id=package.user.id,
                body=request.data,
                amount=request.data.get("amount2"),
                package_self_management=package,
            )

            courses = Course.objects.all()
            for course in courses:
                course.students.add(package.user.id)

            package.status = "active"
            package.save()

            package.user.subscription = "full"
            package.user.save()
        return Response(status=status.HTTP_200_OK)


@method_decorator(swagger_auto_schema(tags=["Payments"]), name="get")
class ListMyPaymentsView(generics.ListAPIView):
    serializer_class = PaymentPackageStripeSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = (
            self.get_serializer_class()
            .Meta.model.objects.filter(
                user_id=1,
            )
            .order_by("-created_at")
        )
        return queryset
