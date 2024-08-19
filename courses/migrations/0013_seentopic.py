# Generated by Django 3.2 on 2022-05-21 19:43

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("courses", "0012_payment_created_at"),
    ]

    operations = [
        migrations.CreateModel(
            name="SeenTopic",
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
                ("topic_id", models.CharField(max_length=10)),
                ("student_id", models.CharField(max_length=10)),
            ],
        ),
    ]
