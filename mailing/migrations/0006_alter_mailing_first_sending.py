# Generated by Django 4.2.2 on 2024-12-24 11:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("mailing", "0005_alter_mailing_recipients"),
    ]

    operations = [
        migrations.AlterField(
            model_name="mailing",
            name="first_sending",
            field=models.DateTimeField(auto_now_add=True, verbose_name="Дата и время первого отправления"),
        ),
    ]
