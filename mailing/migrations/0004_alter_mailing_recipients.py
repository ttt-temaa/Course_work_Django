# Generated by Django 4.2.2 on 2024-12-24 11:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("mailing", "0003_mailing_recipients"),
    ]

    operations = [
        migrations.AlterField(
            model_name="mailing",
            name="recipients",
            field=models.ManyToManyField(
                related_name="recipients",
                to="mailing.recipientmailing",
                verbose_name="Получатели",
            ),
        ),
    ]
