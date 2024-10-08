# Generated by Django 4.1.7 on 2023-05-03 01:56

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("packages", "0012_alter_package_value_and_more"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="demopackage",
            options={"ordering": ["-created_at"]},
        ),
        migrations.AlterModelOptions(
            name="package",
            options={"ordering": ["-created_at"]},
        ),
        migrations.AlterModelOptions(
            name="packageselfmanagement",
            options={"ordering": ["-created_at"]},
        ),
        migrations.AddField(
            model_name="demopackage",
            name="mt_balance",
            field=models.CharField(default=0.0, max_length=50),
            preserve_default=False,
        ),
    ]
