# Generated by Django 5.1.3 on 2025-01-14 16:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("auth_users", "0008_newpassword"),
    ]

    operations = [
        migrations.DeleteModel(
            name="NewPassword",
        ),
    ]
