# Generated by Django 4.1.7 on 2023-05-03 02:35

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("packages", "0015_demopackage_mt_leverage"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="demopackage",
            options={
                "ordering": ["-created_at"],
                "verbose_name_plural": "Packages demo",
            },
        ),
    ]
