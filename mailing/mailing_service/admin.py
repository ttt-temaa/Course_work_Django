from django.contrib import admin
from .models import RecipientMailing, Message, Mailing, MailingAttempt


@admin.register(RecipientMailing)
class RecipientMailingAdmin(admin.ModelAdmin):
    list_display = (
        "email",
        "full_name",
        "comment",
    )


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = (
        "topic_message",
        "message",
    )


@admin.register(Mailing)
class MailingAdmin(admin.ModelAdmin):
    fields = ["start_mailing", "end_mailing", "messages", "recipients"]
    list_display = ("start_mailing", "end_mailing", "messages", "get_recipients")

    def get_recipients(self, obj):
        return "\n".join([p.recipient for p in obj.recipients.all()])


@admin.register(MailingAttempt)
class MailingAttemptAdmin(admin.ModelAdmin):
    list_display = ("datetime_attempt", "status", "mail_server_response", "mailing")
