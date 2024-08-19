# Generated by Django 3.2 on 2022-03-21 14:26

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("courses", "0005_alter_course_slug"),
        ("comments", "0002_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="comment",
            name="course",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="comments",
                to="courses.topic",
            ),
        ),
    ]
