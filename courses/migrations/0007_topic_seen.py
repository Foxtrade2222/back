# Generated by Django 3.2 on 2022-05-07 18:37

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("courses", "0006_auto_20220502_0035"),
    ]

    operations = [
        migrations.AddField(
            model_name="topic",
            name="seen",
            field=models.BooleanField(default=False),
        ),
    ]
