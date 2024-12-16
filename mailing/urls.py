from django.urls import path

from .views import (MailingCreateView, MailingDeleteView, MailingListView, MailingReportView, MailingStartView,
                    MailingStopView, MailingUpdateView, SendMailingView)

urlpatterns = [
    path("", view=MailingListView.as_view(), name="mailings"),
    path("new", view=MailingCreateView.as_view(), name="mailing_new"),
    path("<int:pk>/edit", view=MailingUpdateView.as_view(), name="mailing_edit"),
    path("<int:pk>/delete", view=MailingDeleteView.as_view(), name="mailing_delete"),
    path("<int:pk>/send", view=SendMailingView.as_view(), name="send_mailing"),
    path("<int:pk>/stop", view=MailingStopView.as_view(), name="mailing_stop"),
    path("<int:pk>/start", view=MailingStartView.as_view(), name="mailing_start"),
    path("<int:pk>/report", view=MailingReportView.as_view(), name="mailing_report"),
]
