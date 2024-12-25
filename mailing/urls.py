from django.urls import path
from django.views.decorators.cache import cache_page

from mailing.apps import MailingConfig
from mailing.services import block_mailing, run_mailing
from mailing.views import (
    IndexView,
    MailingAttemptListView,
    MailingCreateView,
    MailingDeleteView,
    MailingDetailView,
    MailingListView,
    MailingUpdateView,
    MessageCreateView,
    MessageDeleteView,
    MessageDetailView,
    MessageListView,
    MessageUpdateView,
    RecipientMailingCreateView,
    RecipientMailingDeleteView,
    RecipientMailingDetailView,
    RecipientMailingListView,
    RecipientMailingUpdateView,
)

app_name = MailingConfig.name

urlpatterns = [
    path("", IndexView.as_view(), name="index"),
    path("mailing/", cache_page(1)(MailingListView.as_view()), name="mailing_list"),
    path(
        "mailing/<int:pk>/detail/",
        cache_page(60)(MailingDetailView.as_view()),
        name="mailing_detail",
    ),
    path("mailing/new/", MailingCreateView.as_view(), name="mailing_create"),
    path("mailing/<int:pk>/edit/", MailingUpdateView.as_view(), name="mailing_update"),
    path("mailing/<int:pk>/delete/", MailingDeleteView.as_view(), name="mailing_delete"),
    path("mailing/<int:pk>/run_mailing/", run_mailing, name="run_mailing"),
    path("block_mailing/<int:pk>", block_mailing, name="block_mailing"),
    path(
        "recipientmailing/",
        cache_page(1)(RecipientMailingListView.as_view()),
        name="recipientmailing_list",
    ),
    path(
        "recipientmailing/<int:pk>/detail/",
        cache_page(60)(RecipientMailingDetailView.as_view()),
        name="recipientmailing_detail",
    ),
    path(
        "recipientmailing/new/",
        RecipientMailingCreateView.as_view(),
        name="recipientmailing_create",
    ),
    path(
        "recipientmailing/<int:pk>/edit/",
        RecipientMailingUpdateView.as_view(),
        name="recipientmailing_update",
    ),
    path(
        "recipientmailing/<int:pk>/delete/",
        RecipientMailingDeleteView.as_view(),
        name="recipientmailing_delete",
    ),
    path("message/", cache_page(60)(MessageListView.as_view()), name="message_list"),
    path(
        "message/<int:pk>/detail/",
        cache_page(60)(MessageDetailView.as_view()),
        name="message_detail",
    ),
    path("message/new/", MessageCreateView.as_view(), name="message_create"),
    path("message/<int:pk>/edit/", MessageUpdateView.as_view(), name="message_update"),
    path("message/<int:pk>/delete/", MessageDeleteView.as_view(), name="message_delete"),
    path("attempt/", cache_page(60)(MailingAttemptListView.as_view()), name="attempt"),
]
