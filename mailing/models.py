from django.db import models


class Mailing(models.Model):
    STATUS_CHOICES = (
        ("CREATED", "Создана"),
        ("STARTED", "Запущена"),
        ("FINISHED", "Завершена"),
    )
    start_time = models.DateTimeField(verbose_name="Дата и время запуска")
    end_time = models.DateTimeField(verbose_name="Дата и время окончания")
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="CREATED", verbose_name="Статус")
    message = models.ForeignKey("messages_mailing.Message", on_delete=models.CASCADE, verbose_name="Сообщение")
    recipients = models.ManyToManyField("recipients.Recipient", related_name="mailings", verbose_name="Получатели")
    owner = models.ForeignKey(
        "accounts.User", related_name="mailings", on_delete=models.CASCADE, verbose_name="Владелец"
    )

    def __str__(self):
        return f"Mailing #{self.id} - {self.status}"

    class Meta:
        verbose_name = "Рассылка"
        verbose_name_plural = "Рассылки"
        ordering = ["id"]
        permissions = [
            ("view_all_mailings", "Can view all mailings"),
        ]


class MailingAttempt(models.Model):
    STATUS_CHOICES = (
        ("SUCCESS", "Успешно"),
        ("FAILURE", "Не успешно"),
    )
    attempt_time = models.DateTimeField(auto_now_add=True, verbose_name="Время попытки")
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="SUCCESS", verbose_name="Статус")
    response = models.TextField(blank=True, verbose_name="Ответ")
    mailing = models.ForeignKey(Mailing, on_delete=models.CASCADE, verbose_name="Рассылка")

    def __str__(self):
        return f"Attempt {self.id} - {self.status} at {self.attempt_time}"

    class Meta:
        verbose_name = "Попытка рассылки"
        verbose_name_plural = "Попытки рассылки"
        ordering = ["id"]
