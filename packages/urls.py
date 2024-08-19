from django.urls import path

from packages.views import (
    CreateDemoPackageView,
    CreatePackageSelfManagementView,
    CreatePackageView,
    ListMyPackagesDemoView,
    ListMyPackagesSelfManagementView,
    ListMyPackagesView,
    ListPackagesSelfManagementView,
    ListPackagesView,
    RetrievePackageDemoView,
    RetrievePackageSelfManagementView,
    RetrievePackageView,
    UpdatePackageView,
)

app_name = "package"
urlpatterns = [
    path(
        "create/demo/package/",
        CreateDemoPackageView.as_view(),
    ),
    path(
        "create/package/",
        CreatePackageView.as_view(),
    ),
    path(
        "retrieve/package/<int:pk>/",
        RetrievePackageView.as_view(),
    ),
    path(
        "create/package-self-management/",
        CreatePackageSelfManagementView.as_view(),
    ),
    path(
        "retrieve/package-self-management/<int:pk>/",
        RetrievePackageSelfManagementView.as_view(),
    ),
    path(
        "update/package/<int:pk>/",
        UpdatePackageView.as_view(),
    ),
    path(
        "list/my/packages/",
        ListMyPackagesView.as_view(),
    ),
    path(
        "list/my/package-self-management/",
        ListMyPackagesSelfManagementView.as_view(),
    ),
    path(
        "retrieve/package-demo/<int:pk>/",
        RetrievePackageDemoView.as_view(),
    ),
    path(
        "list/my/packages-demo/",
        ListMyPackagesDemoView.as_view(),
    ),
    path(
        "list/packages/",
        ListPackagesView.as_view(),
    ),
    path(
        "list/package-self-management/",
        ListPackagesSelfManagementView.as_view(),
    ),
]
