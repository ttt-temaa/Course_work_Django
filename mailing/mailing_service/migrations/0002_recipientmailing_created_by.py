# Generated by Django 5.1.3 on 2025-01-13 10:12

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("mailing_service", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name="recipientmailing",
            name="created_by",
            field=models.ForeignKey(
                default=40,
                editable=False,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="%(class)s_created",
                to=settings.AUTH_USER_MODEL,
                verbose_name="Created By",
            ),
            preserve_default=False,
        ),
    ]
