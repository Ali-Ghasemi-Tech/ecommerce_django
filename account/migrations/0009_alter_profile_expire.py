# Generated by Django 5.1.6 on 2025-03-18 11:18


import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("account", "0008_alter_profile_email_verification_token_and_more"),

    ]

    operations = [
        migrations.AlterField(

            model_name="profile",
            name="expire",
            field=models.DateTimeField(
                default=datetime.datetime(
                    2025, 3, 18, 11, 23, 58, 433322, tzinfo=datetime.timezone.utc
                )
            ),

        ),
    ]
