# Generated by Django 4.2.2 on 2024-12-24 11:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("mailing", "0006_alter_mailing_first_sending"),
    ]

    operations = [
        migrations.AlterField(
            model_name="mailing",
            name="first_sending",
            field=models.DateTimeField(verbose_name="Дата и время первого отправления"),
        ),
        migrations.AlterField(
            model_name="mailing",
            name="status",
            field=models.CharField(
                choices=[
                    ("Создана", "Создана"),
                    ("Запущена", "Запущена"),
                    ("Завершена", "Завершена"),
                ],
                default="Создана",
                max_length=10,
                verbose_name="Статус рассылки",
            ),
        ),
    ]
