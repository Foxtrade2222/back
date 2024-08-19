from django_filters import rest_framework as filters

from users.serializers import AllUserSerializer


class UserFilter(filters.FilterSet):
    first_name = filters.CharFilter(field_name="first_name", lookup_expr="icontains")
    last_name = filters.CharFilter(field_name="last_name", lookup_expr="icontains")
    email = filters.CharFilter(field_name="email", lookup_expr="icontains")
    rol = filters.CharFilter(field_name="rol", lookup_expr="icontains")
    subscription = filters.CharFilter(
        field_name="subscription", lookup_expr="icontains"
    )
    identity_card = filters.CharFilter(
        field_name="identity_card", lookup_expr="icontains"
    )
    phone_number = filters.CharFilter(
        field_name="phone_number", lookup_expr="icontains"
    )
    image_profile = filters.CharFilter(
        field_name="image_profile", lookup_expr="icontains"
    )
    username = filters.CharFilter(field_name="username", lookup_expr="icontains")
    birth_date = filters.DateFilter(field_name="birth_date")
    deferred_name = filters.CharFilter(
        field_name="deferred_name", lookup_expr="icontains"
    )
    deferred_document_number = filters.CharFilter(
        field_name="deferred_document_number", lookup_expr="icontains"
    )
    country_code = filters.CharFilter(
        field_name="country_code", lookup_expr="icontains"
    )
    address = filters.CharFilter(field_name="address", lookup_expr="icontains")
    city = filters.CharFilter(field_name="city", lookup_expr="icontains")
    state = filters.CharFilter(field_name="state", lookup_expr="icontains")
    country = filters.CharFilter(field_name="country", lookup_expr="icontains")
    referral_code = filters.CharFilter(
        field_name="referral_code", lookup_expr="icontains"
    )
    since = filters.DateTimeFilter(field_name="date_joined", lookup_expr="gte")
    until = filters.DateTimeFilter(field_name="date_joined", lookup_expr="lte")

    class Meta:
        model = AllUserSerializer.Meta.model
        fields = AllUserSerializer.Meta.fields
