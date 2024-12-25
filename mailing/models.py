from django.db import models

from users.models import User

NULLABLE = {"blank": True, "null": True}


class RecipientMailing(models.Model):
    email = models.EmailField(max_length=255, unique=True, verbose_name="E-mail")
    fio = models.CharField(max_length=255, verbose_name="ФИО")
    comment = models.TextField(verbose_name="Комментарий", **NULLABLE)
    avatar = models.ImageField(upload_to="mailing/avatars", **NULLABLE, verbose_name="Аватар")
    is_active = models.BooleanField(default=True, verbose_name="активность")
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, **NULLABLE, verbose_name="Владелец")

    def __str__(self):
        return f"{self.fio} <{self.email}>"

    class Meta:
        verbose_name = "Получатель рассылки"
        verbose_name_plural = "Получатели рассылки"
        ordering = ["fio"]


class Message(models.Model):
    subject = models.CharField(max_length=255, verbose_name="Тема сообщения")
    content = models.TextField(verbose_name="Содержание сообщения")
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, **NULLABLE, verbose_name="Владелец")

    def __str__(self):
        return self.content

    class Meta:
        verbose_name = "Сообщение"
        verbose_name_plural = "Сообщения"
        ordering = ["subject"]


class Mailing(models.Model):
    CREATED = "Создана"
    LAUNCHED = "Запущена"
    COMPLETED = "Завершена"

    STATUS_CHOICES = [
        (CREATED, "Создана"),
        (LAUNCHED, "Запущена"),
        (COMPLETED, "Завершена"),
    ]

    first_sending = models.DateTimeField(verbose_name="Дата и время первого отправления")
    end_sending = models.DateTimeField(verbose_name="Дата и время окончания отправки")
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default=CREATED,
        verbose_name="Статус рассылки",
    )
    message = models.ForeignKey(
        Message,
        on_delete=models.CASCADE,
        verbose_name="Сообщение",
        related_name="mailings",
    )
    recipients = models.ManyToManyField(
        RecipientMailing,
        related_name="recipients",
        verbose_name="Получатели",
        help_text="Укажите получателей рассылки (используйте CTRL или COMMAND)",
    )
    is_active = models.BooleanField(default=True, verbose_name="активна")
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, **NULLABLE, verbose_name="Владелец")

    def __str__(self):
        return f"Рассылка {self.id}"

    class Meta:
        verbose_name = "Рассылка"
        verbose_name_plural = "Рассылки"
        ordering = ["first_sending"]
        permissions = [
            ("can_disable_mailing", "Возможность отключения рассылки"),
        ]


class MailingAttempt(models.Model):
    """Попытка рассылки"""

    STATUS_OK = "Успешно"
    STATUS_NOK = "Не успешно"

    STATUS_CHOICES = [
        (STATUS_OK, "Успешно"),
        (STATUS_NOK, "Не успешно"),
    ]

    date_attempt = models.DateTimeField(verbose_name="Дата и время попытки")
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, verbose_name="Статус попытки")
    server_response = models.TextField(verbose_name="Ответ почтового сервера")
    mailing = models.ForeignKey(
        Mailing,
        on_delete=models.CASCADE,
        verbose_name="Рассылка",
        related_name="mailing",
    )
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, **NULLABLE, verbose_name="Владелец")

    def __str__(self):
        return f"{self.date_attempt} <{self.status}>"

    class Meta:
        verbose_name = "Попытка"
        verbose_name_plural = "Попытки"
        ordering = ["date_attempt", "status"]
