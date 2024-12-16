from django.conf.urls import include
from django.contrib import admin
from django.urls import path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("main.urls")),
    path("accounts/", include("accounts.urls")),
    path("recipients/", include("recipients.urls")),
    path("messages/", include("messages_mailing.urls")),
    path("mailings/", include("mailing.urls")),
]
