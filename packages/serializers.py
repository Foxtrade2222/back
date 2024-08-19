import requests
from django.contrib.auth import get_user_model
from rest_framework import serializers

from packages.models import DemoPackage, Package, PackageSelfManagement

User = get_user_model()


class PackageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Package
        fields = [
            "id",
            "currencies",
            "balance",
            "account_type",
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
            "value",
            "end_date",
            "mt_login",
            "mt_password",
            "mt_password_investor",
            "mt_server",
            "mt_windows",
            "mt_ios",
            "mt_web",
        ]


class PackageAccountInfoSerializer(serializers.ModelSerializer):
    mt_account_info = serializers.SerializerMethodField()

    class Meta:
        model = Package
        fields = [
            "id",
            "currencies",
            "balance",
            "account_type",
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
            "value",
            "end_date",
            "mt_login",
            "mt_password",
            "mt_password_investor",
            "mt_server",
            "mt_windows",
            "mt_ios",
            "mt_web",
            "mt_account_info",
        ]

    def get_mt_account_info(self, obj):
        if obj.status == "active" and obj.mt_login != "" and obj.mt_password != "":
            login = obj.mt_login
            password = obj.mt_password
            response = requests.get(
                "https://d32f-109-205-61-126.ngrok-free.app/account-info",
                params={
                    "login": login,
                    "password": password,
                },
                headers={"token": "6tUChM3PTU0frfPPs4RzSscQrVU"},
            )
            if response.status_code == 200:
                return response.json()
        return None


class CreatePackageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Package
        fields = (
            "currencies",
            "balance",
            "account_type",
            "first_name",
            "last_name",
            "email",
            "phone_number",
            "city",
            "country",
            "postal_code",
            "tos",
            "cancellation_policies",
        )


class UpdatePackageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Package
        fields = (
            "currencies",
            "balance",
            "account_type",
            "first_name",
            "last_name",
            "email",
            "phone_number",
            "city",
            "country",
            "postal_code",
            "status",
            "tos",
            "cancellation_policies",
            "end_date",
            "mt_login",
            "mt_password",
            "mt_password_investor",
            "mt_server",
        )


class PackageSelfManagementSerializer(serializers.ModelSerializer):
    referral_code_owner_name = serializers.SerializerMethodField(read_only=True)
    referral_code_owner_identity_card = serializers.SerializerMethodField(
        read_only=True
    )

    def get_referral_code_owner_name(self, obj):
        u = User.objects.filter(referral_code=obj.referral_code).first()

        if u is None:
            return None

        return f"{u.first_name} {u.last_name}"

    def get_referral_code_owner_identity_card(self, obj):
        u = User.objects.filter(referral_code=obj.referral_code).first()

        if u is None:
            return None

        return u.identity_card

    class Meta:
        model = PackageSelfManagement
        fields = [
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
            "referral_code_owner_name",
            "referral_code_owner_identity_card",
            "created_at",
        ]


class CreatePackageSelfManagementSerializer(serializers.ModelSerializer):
    class Meta:
        model = PackageSelfManagement
        fields = (
            "package_type",
            "first_name",
            "last_name",
            "email",
            "phone_number",
            "city",
            "country",
            "postal_code",
            "tos",
            "cancellation_policies",
            "referral_code",
        )


class FullPackageSerializer(serializers.Serializer):
    self_management = PackageSelfManagementSerializer(many=True)
    trader = PackageSerializer(many=True)


class CreateDemoAccountSerializer(serializers.Serializer):
    balance = serializers.CharField()


class PackageDemoSerializer(serializers.ModelSerializer):
    class Meta:
        model = DemoPackage
        fields = "__all__"


class PackageDemoAccountInfoSerializer(serializers.ModelSerializer):
    mt_account_info = serializers.SerializerMethodField()

    class Meta:
        model = DemoPackage
        fields = "__all__"

    def get_mt_account_info(self, obj):
        if obj.mt_login != "" and obj.mt_password != "":
            login = obj.mt_login
            password = obj.mt_password
            response = requests.get(
                "https://d32f-109-205-61-126.ngrok-free.app/account-info",
                params={
                    "login": login,
                    "password": password,
                },
                headers={"token": "6tUChM3PTU0frfPPs4RzSscQrVU"},
            )
            if response.status_code == 200:
                return response.json()
        return None
