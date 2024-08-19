from django.apps import AppConfig


class PackagesConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "packages"

    def ready(self) -> None:
        import packages.signals  # noqa
