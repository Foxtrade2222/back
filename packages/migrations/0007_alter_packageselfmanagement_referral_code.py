# Generated by Django 4.1.7 on 2023-04-09 01:51

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("packages", "0006_alter_package_options_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="packageselfmanagement",
            name="referral_code",
            field=models.CharField(max_length=20),
        ),
    ]
