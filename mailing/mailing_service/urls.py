from django.urls import path

from . import views

app_name = "mailing_service"

urlpatterns = [
    path("recipients_mailing_views/", views.RecipientListView.as_view(), name="recipients_mailing_views"),
    path(
        "form_create_recipient_mailing_views/",
        views.RecipientCreateView.as_view(),
        name="form_create_recipient_mailing_views",
    ),
    path("update_recipient_views/<int:pk>/", views.RecipientUpdateView.as_view(), name="update_recipient_views"),
    path("detail_recipient_views/<int:pk>/", views.RecipientDetailView.as_view(), name="detail_recipient_views"),
    path(
        "detail_recipient_views/<int:pk>/delete_recipient_views",
        views.RecipientDeleteView.as_view(),
        name="delete_recipient_views",
    ),
    path("messages_views/", views.MessageListView.as_view(), name="messages_views"),
    path("form_create_message_views/", views.MessageCreateView.as_view(), name="form_create_message_views"),
    path("detail_message_views/<int:pk>/", views.MessageDetailView.as_view(), name="detail_message_views"),
    path("update_message_views/<int:pk>/", views.MessageUpdateView.as_view(), name="update_message_views"),
    path(
        "detail_message_views/<int:pk>/delete_message_views/",
        views.MessageDeleteView.as_view(),
        name="delete_message_views",
    ),
    path("form_create_mailing_views/", views.MailingCreateView.as_view(), name="form_create_mailing_views"),
    path("mailing_views/", views.MailListView.as_view(), name="mailing_views"),
    path("detail_mailing_views/<int:pk>/", views.MailingDetailView.as_view(), name="detail_mailing_views"),
    path("update_mailing_views/<int:pk>/", views.MailingUpdateView.as_view(), name="update_mailing_views"),
    path(
        "detail_mailing_views/<int:pk>/delete_mailing_views/",
        views.MailingDeleteView.as_view(),
        name="delete_mailing_views",
    ),
    path("disable_mailing_views/<int:pk>/", views.DisableMailingView.as_view(), name="disable_mailing_views"),
    path("detail_mailing_views/<int:pk>/send_mail_views/", views.SendMailView.as_view(), name="send_mail_views"),
    path("home_views/", views.MailingListView.as_view(), name="home_views"),
    path(
        "detail_mailing_views/<int:pk>/not_found_recipients_views/",
        views.NotFoundRecipientsView.as_view(),
        name="not_found_recipients_views",
    ),
]
