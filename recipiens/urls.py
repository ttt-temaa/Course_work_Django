from django.urls import path

from .views import RecipientCreateView, RecipientDeleteView, RecipientListView, RecipientUpdateView

urlpatterns = [
    path("", RecipientListView.as_view(), name="recipients"),
    path("new", RecipientCreateView.as_view(), name="recipient_new"),
    path("<int:pk>/edit", RecipientUpdateView.as_view(), name="recipient_edit"),
    path("<int:pk>/delete", RecipientDeleteView.as_view(), name="recipient_delete"),
]
