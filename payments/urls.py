from django.urls import path

from payments.views import (
    CreatePaymentPackageCoinpaymentView,
    CreatePaymentPackageSelfManagementCoinpaymentView,
    CreatePaymentPackageSelfManagementStripeView,
    CreatePaymentPackageStripeView,
    IPNPackageCoinpaymentView,
    IPNSelfManagementPackageCoinpaymentView,
    ListMyPaymentsView,
)

app_name = "payments"
urlpatterns = [
    path(
        "payment/package/stripe",
        CreatePaymentPackageStripeView.as_view(),
    ),
    path(
        "payment/package/coinpayments",
        CreatePaymentPackageCoinpaymentView.as_view(),
    ),
    path(
        "ipn/package/coinpayments/<int:package_id>",
        IPNPackageCoinpaymentView.as_view(),
        name="ipn_package",
    ),
    path(
        "payment/package-self-management/stripe",
        CreatePaymentPackageSelfManagementStripeView.as_view(),
    ),
    path(
        "payment/package-self-management/coinpayments",
        CreatePaymentPackageSelfManagementCoinpaymentView.as_view(),
    ),
    path(
        "ipn/package-self-management/coinpayments/<int:package_id>",
        IPNSelfManagementPackageCoinpaymentView.as_view(),
        name="ipn_package_self_management",
    ),
    # Crear endpoint para admin y devolver todos los payments realizados
    path(
        "list/my/payments",
        ListMyPaymentsView.as_view(),
    ),
]
