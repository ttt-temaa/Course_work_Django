from django.db import models


# Create your models here.
class Message(models.Model):
    subject = models.CharField(max_length=255, blank=True, verbose_name="Тема сообщения")
    body = models.TextField(verbose_name="Текст сообщения")
    owner = models.ForeignKey("accounts.User", on_delete=models.CASCADE, verbose_name="Владелец")

    def __str__(self):
        return self.subject

    class Meta:
        verbose_name = "Сообщение"
        verbose_name_plural = "Сообщения"
        ordering = ["id"]
        permissions = [
            ("view_all_messages", "Can view all messages"),
        ]
