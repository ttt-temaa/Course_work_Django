from django.core.mail import send_mail
from django.core.management.base import BaseCommand

from mailing_service.models import Mailing


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        mailing = Mailing.objects.filter(id="")[0]
        try:
            send_mail(
                mailing.messages.topic_message,
                mailing.messages.message,
                "serega94nn@yandex.ru",
                [i.email for i in mailing.recipients.all()],
            )
        except Exception:
            print("Проверьте правильность ввода данных")
