# Generated by Django 4.1.7 on 2023-04-09 01:38

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models

import users.fields


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("packages", "0004_rename_ios_package_mt_ios_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="PackageSelfManagement",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("pending", "Pending"),
                            ("closed", "Closed"),
                            ("active", "Active"),
                        ],
                        max_length=20,
                    ),
                ),
                (
                    "PACKAGE_type",
                    models.CharField(
                        choices=[("ag", "ICEX AG")], default="ag", max_length=2
                    ),
                ),
                ("first_name", models.CharField(max_length=50)),
                ("last_name", models.CharField(max_length=50)),
                ("email", users.fields.LowerCaseEmailField(max_length=254)),
                ("phone_number", models.CharField(blank=True, max_length=20)),
                ("address", models.CharField(blank=True, max_length=50)),
                ("city", models.CharField(blank=True, max_length=10)),
                ("country", models.CharField(blank=True, max_length=10)),
                ("postal_code", models.CharField(blank=True, max_length=10)),
                ("tos", models.BooleanField(default=False)),
                ("cancellation_policies", models.BooleanField(default=False)),
                ("referral_code", models.CharField(blank=True, max_length=20)),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="packages_self_management",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]
