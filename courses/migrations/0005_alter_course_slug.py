# Generated by Django 3.2 on 2022-02-23 03:31

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("courses", "0004_auto_20220222_0236"),
    ]

    operations = [
        migrations.AlterField(
            model_name="course",
            name="slug",
            field=models.SlugField(blank=True, max_length=100),
        ),
    ]
