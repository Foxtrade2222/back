import string

from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.password_validation import validate_password
from django.utils.crypto import get_random_string
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from packages.serializers import (
    PackageDemoSerializer,
    PackageSelfManagementSerializer,
    PackageSerializer,
)
from utils.hashids import encode_pk
from utils.resend import (
    send_reset_password,
    send_welcome_email,
)


User = get_user_model()


# Pendiente de moficiar los fields permitidos
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"


class PublicUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "first_name",
            "last_name",
            "image_profile",
        )


class SignUpUserSerializer(serializers.ModelSerializer):
    username = serializers.EmailField(
        required=True, validators=[UniqueValidator(queryset=User.objects.all())]
    )

    class Meta:
        model = User
        fields = (
            "first_name",
            "last_name",
            "username",
            "password",
            "identity_card",
            "phone_number",
            "birth_date",
            "deferred_name",
            "deferred_document_number",
            "country_code",
            "address",
            "city",
            "state",
            "country",
        )
        extra_kwargs = {
            "password": {"write_only": True},
        }

    def create(self, validated_data):
        user = self.Meta.model.objects.create_user(**validated_data)
        try:
            send_welcome_email(
                email=user.username,
                first_name=user.first_name,
                password=validated_data["password"],
            )
        except Exception as err:
            print(err)
        return user


class LoginUserSerializer(serializers.Serializer):
    username = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, data):
        user = authenticate(**data)
        if user and not user.referral_code:
            user.referral_code = encode_pk(user.id)
            user.save()
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Invalid details.")


class ResetPasswordSerializer(serializers.Serializer):
    username = serializers.EmailField()

    def create(self, validated_data):
        try:
            user = User.objects.get(
                username__iexact=validated_data.get("username", None)
            )
            random_password = get_random_string(
                8,
                allowed_chars=string.ascii_lowercase
                + string.ascii_uppercase
                + string.digits,
            )
            user.set_password(random_password)
            user.save()
            send_reset_password(
                email=user.username,
                first_name=user.first_name,
                password=random_password,
            )
            return user
        except User.DoesNotExist:
            raise serializers.ValidationError("Mail not available")


class UpdateUserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "first_name",
            "last_name",
            "username",
            "identity_card",
            "phone_number",
            "image_profile",
            "identity_card",
            "phone_number",
            "birth_date",
            "deferred_name",
            "deferred_document_number",
            "country_code",
            "address",
            "city",
            "state",
            "country",
        )


class AllUserSerializer(serializers.ModelSerializer):
    packages = PackageSerializer(many=True)
    packages_self_management = PackageSelfManagementSerializer(many=True)
    demo_package = PackageDemoSerializer()

    class Meta:
        model = User
        fields = (
            "id",
            "first_name",
            "last_name",
            "email",
            "rol",
            "subscription",
            "identity_card",
            "phone_number",
            "image_profile",
            "username",
            "birth_date",
            "deferred_name",
            "deferred_document_number",
            "country_code",
            "address",
            "city",
            "state",
            "country",
            "referral_code",
            "date_joined",
            "packages",
            "packages_self_management",
            "demo_package",
        )


class UpdateUserSerializer(serializers.ModelSerializer):
    courses_ids = serializers.ListField(
        child=serializers.IntegerField(),
        default=[],
    )

    class Meta:
        model = User
        fields = (
            "id",
            "first_name",
            "last_name",
            "email",
            "rol",
            "subscription",
            "identity_card",
            "phone_number",
            "image_profile",
            "username",
            "birth_date",
            "courses_ids",
            "deferred_name",
            "deferred_document_number",
            "country_code",
            "address",
            "city",
            "state",
            "country",
        )


class CreateUserByAdmin(serializers.ModelSerializer):
    username = serializers.EmailField(
        required=True, validators=[UniqueValidator(queryset=User.objects.all())]
    )
    courses_ids = serializers.ListField(
        child=serializers.IntegerField(),
        default=[],
    )

    class Meta:
        model = User
        fields = (
            "first_name",
            "last_name",
            "username",
            "rol",
            "image_profile",
            "identity_card",
            "courses_ids",
            "birth_date",
            "deferred_name",
            "deferred_document_number",
            "country_code",
            "address",
            "city",
            "state",
            "country",
        )

    def create(self, validated_data):
        del validated_data["courses_ids"]
        random_password = get_random_string(
            8,
            allowed_chars=string.ascii_lowercase
            + string.ascii_uppercase
            + string.digits,
        )
        validated_data["password"] = random_password
        user = self.Meta.model.objects.create_user(**validated_data)
        send_welcome_email(
            email=user.username,
            first_name=user.first_name,
            password=validated_data["password"],
        )
        return user


class ChangePasswordSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password]
    )
    old_password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = (
            "old_password",
            "password",
        )

    def validate_old_password(self, value):
        user = self.context["request"].user
        if not user.check_password(value):
            raise serializers.ValidationError({"message": "Contraseña incorrecta"})
        return value

    def update(self, instance, validated_data):
        instance.set_password(validated_data["password"])
        instance.save()

        return instance


class StatisticsSerializer(serializers.Serializer):
    total_admins = serializers.IntegerField()
    total_students = serializers.IntegerField()
    total_teachers = serializers.IntegerField()
    total_subscribers = serializers.IntegerField()
    date = serializers.DateTimeField()
    users = serializers.IntegerField()
