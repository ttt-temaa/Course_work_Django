from django.contrib import admin

from .models import Recipient


# Register your models here.
@admin.register(Recipient)
class RecipientAdmin(admin.ModelAdmin):
    list_display = ("email", "full_name", "comment")
    search_fields = ("email", "full_name")
    list_filter = ("email", "full_name")
