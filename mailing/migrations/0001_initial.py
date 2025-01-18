# Generated by Django 5.1.4 on 2025-18-01 13:30

import datetime
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Mailing",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "first_send_at",
                    models.DateTimeField(
                        default=datetime.datetime(2024, 12, 9, 18, 30, 36, 244044),
                        verbose_name="Дата и время первой отправки",
                    ),
                ),
                (
                    "finish_send_at",
                    models.DateTimeField(
                        default=datetime.datetime(2024, 12, 10, 18, 30, 36, 244044),
                        verbose_name="Дата и время окончания отправки",
                    ),
                ),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("completed", "Завершена"),
                            ("created", "Создана"),
                            ("running", "Запущена"),
                        ],
                        max_length=9,
                        verbose_name="Статус рассылки",
                    ),
                ),
                (
                    "owner",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="mailing_owner",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="Владелец",
                    ),
                ),
            ],
            options={
                "verbose_name": "Сообщение",
                "verbose_name_plural": "Сообщения",
                "ordering": ["id"],
                "permissions": [("can_cancel_mailing", "Can cancel mailing")],
            },
        ),
        migrations.CreateModel(
            name="MailingAttempt",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "attempted_at",
                    models.DateTimeField(verbose_name="Дата и время попытки отправки"),
                ),
                (
                    "status",
                    models.CharField(
                        choices=[("success", "Успешно"), ("failure", "Не успешно")],
                        max_length=7,
                        verbose_name="Статус",
                    ),
                ),
                (
                    "mailing_response",
                    models.TextField(
                        blank=True, null=True, verbose_name="Ответ сервера"
                    ),
                ),
                (
                    "mailing",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="attempts",
                        to="mailing.mailing",
                        verbose_name="Рассылка",
                    ),
                ),
            ],
            options={
                "verbose_name": "Попытка рассылки",
                "verbose_name_plural": "Попытки рассылки",
                "ordering": ["id"],
            },
        ),
        migrations.CreateModel(
            name="Message",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("title", models.CharField(max_length=200, verbose_name="Тема письма")),
                ("message", models.TextField(verbose_name="Тело письма")),
                (
                    "owner",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="message_owner",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="Владелец",
                    ),
                ),
            ],
            options={
                "verbose_name": "Сообщение",
                "verbose_name_plural": "Сообщения",
                "ordering": ["id"],
            },
        ),
        migrations.AddField(
            model_name="mailing",
            name="message",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="mailing",
                to="mailing.message",
                verbose_name="Сообщение",
            ),
        ),
        migrations.CreateModel(
            name="Recipient",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "email",
                    models.EmailField(
                        help_text="Адрес почты должен быть уникальным",
                        max_length=254,
                        unique=True,
                        verbose_name="Почта",
                    ),
                ),
                ("full_name", models.CharField(max_length=200, verbose_name="ФИО")),
                (
                    "comment",
                    models.TextField(blank=True, null=True, verbose_name="Комментарий"),
                ),
                (
                    "owner",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="recipients_owner",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="Владелец",
                    ),
                ),
            ],
            options={
                "verbose_name": "Получатель рассылки",
                "verbose_name_plural": "Получатели рассылки",
                "ordering": ["id"],
            },
        ),
        migrations.AddField(
            model_name="mailing",
            name="recipients",
            field=models.ManyToManyField(
                related_name="mailing",
                to="mailing.recipient",
                verbose_name="Получатели",
            ),
        ),
    ]
