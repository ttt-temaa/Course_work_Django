from django.contrib import admin

from .models import Message


# Register your models here.
@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ("subject", "body")
    search_fields = ("subject", "body")
    list_filter = ("subject", "body")
    ordering = ("id",)
