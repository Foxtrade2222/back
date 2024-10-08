# Generated by Django 3.2 on 2022-05-22 22:46

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("courses", "0014_seentopic_created_at"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="seentopic",
            name="topic_id",
        ),
        migrations.AddField(
            model_name="seentopic",
            name="topics",
            field=models.ForeignKey(
                default=1,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="seens",
                to="courses.topic",
            ),
            preserve_default=False,
        ),
    ]
