from django.db import models

from auth_users.models import CustomUser


# Create your models here.


class CreatedByMixin(models.Model):

    created_by = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name="%(class)s_created",
        verbose_name="Created By",
        editable=False,
    )

    class Meta:
        abstract = True


class RecipientMailing(CreatedByMixin, models.Model):
    email = models.EmailField(max_length=100, verbose_name="Email")
    full_name = models.CharField(verbose_name="ФИО")
    comment = models.TextField(verbose_name="Комментарий")

    def __str__(self):
        return f"{self.email}"

    class Meta:
        verbose_name = "получатель"
        verbose_name_plural = "получатели"
        db_table = "recipient_mailing"
        permissions = [("can_view_all_recipient_lists", "can view all recipient lists")]


class Message(CreatedByMixin, models.Model):
    topic_message = models.CharField(verbose_name="Тема письма")
    message = models.TextField(verbose_name="Содержание письма")

    def __str__(self):
        return f"{self.topic_message}"

    class Meta:
        verbose_name = "письмо"
        verbose_name_plural = "письма"
        db_table = "message"
        permissions = [("can_view_all_message_lists", "can view all message lists")]


class Mailing(CreatedByMixin, models.Model):
    start_mailing = models.DateTimeField(verbose_name="Дата время начала рассылки")
    end_mailing = models.DateTimeField(verbose_name="Дата время окончания рассылки")
    status = models.CharField(verbose_name="Статус рассылки", default="Создана")
    messages = models.ForeignKey(
        "Message", on_delete=models.CASCADE, related_name="link_on_message", max_length=100, verbose_name="Письмо"
    )
    recipients = models.ManyToManyField("RecipientMailing", verbose_name="Получатели", related_name="recipients")

    def __str__(self):
        return f"{self.messages} - {self.recipients}"

    class Meta:
        verbose_name = "рассылка"
        verbose_name_plural = "рассылки"
        db_table = "mailing"
        permissions = [
            ("can_disable_mailing", "can disable mailing"),
            ("can_view_all_mailing_lists", "can view all mailing lists"),
        ]


class MailingAttempt(models.Model):
    datetime_attempt = models.DateTimeField(auto_now_add=True)
    status = models.CharField(verbose_name="Статус рассылки")
    mail_server_response = models.TextField(verbose_name="Ответ почтового сервера")
    mailing = models.ForeignKey(Mailing, on_delete=models.CASCADE, related_name="mailing")

    class Meta:
        verbose_name = "попытка рассылки"
        verbose_name_plural = "попытки рассылки"
        db_table = "mailing_attempt"
