# Generated by Django 4.2.2 on 2024-12-24 11:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("mailing", "0008_recipientmailing_avatar"),
    ]

    operations = [
        migrations.AlterField(
            model_name="mailingattempt",
            name="status",
            field=models.CharField(
                choices=[("Успешно", "Успешно"), ("Не успешно", "Не успешно")],
                max_length=15,
                verbose_name="Статус попытки",
            ),
        ),
    ]
