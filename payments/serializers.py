from rest_framework import serializers

from packages.serializers import PackageSelfManagementSerializer, PackageSerializer
from payments.models import Payment


class CreatePaymentPackageStripeSerializer(serializers.Serializer):
    package_id = serializers.CharField()
    token_id = serializers.CharField()


class CreatePaymentPackageCoinpaymentSerializer(serializers.Serializer):
    package_id = serializers.CharField()
    currency2 = serializers.CharField()


class CreatePaymentPackageSelfManagementStripeSerializer(serializers.Serializer):
    package_self_management_id = serializers.CharField()
    token_id = serializers.CharField()


class CreatePaymentPackageSelfManagementCoinpaymentSerializer(serializers.Serializer):
    package_self_management_id = serializers.CharField()
    currency2 = serializers.CharField()


class PaymentPackageStripeSerializer(serializers.ModelSerializer):
    package = PackageSerializer()
    package_self_management = PackageSelfManagementSerializer()

    class Meta:
        model = Payment
        fields = [
            "id",
            "payment_option",
            "package",
            "package_self_management",
            "body",
            "amount",
            "created_at",
        ]


class PaymentSerializer(serializers.ModelSerializer):
    package = PackageSerializer()
    package_self_management = PackageSelfManagementSerializer()

    class Meta:
        model = Payment
        fields = [
            "id",
            "payment_option",
            "package",
            "package_self_management",
            "body",
            "amount",
            "created_at",
        ]
