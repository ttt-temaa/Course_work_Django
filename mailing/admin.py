from django.contrib import admin

from .models import Mailing, MailingAttempt


# Register your models here.
@admin.register(Mailing)
class MailingAdmin(admin.ModelAdmin):
    list_display = ("status", "message", "start_time", "end_time")
    list_filter = ("status", "message", "recipients", "start_time", "end_time")
    search_fields = ("status", "message", "recipients", "start_time", "end_time")
    ordering = ("-start_time",)


@admin.register(MailingAttempt)
class MailingAttemptAdmin(admin.ModelAdmin):
    list_display = ("mailing", "status", "response", "attempt_time")
    list_filter = ("status", "attempt_time")
    search_fields = ("mailing", "response")
    ordering = ("-attempt_time",)
