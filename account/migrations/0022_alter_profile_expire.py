# Generated by Django 5.1.7 on 2025-03-26 19:40

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("account", "0021_alter_profile_expire"),
    ]

    operations = [
        migrations.AlterField(
            model_name="profile",
            name="expire",
            field=models.DateTimeField(
                default=datetime.datetime(
                    2025, 3, 26, 19, 45, 34, 817309, tzinfo=datetime.timezone.utc
                )
            ),
        ),
    ]
