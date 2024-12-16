from django.urls import path

from .views import MessageCreateView, MessageDeleteView, MessageListView, MessageUpdateView

urlpatterns = [
    path("", view=MessageListView.as_view(), name="messages"),
    path("new", view=MessageCreateView.as_view(), name="message_new"),
    path("<int:pk>/edit", view=MessageUpdateView.as_view(), name="message_edit"),
    path("<int:pk>/delete", view=MessageDeleteView.as_view(), name="message_delete"),
]
