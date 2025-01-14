from smtplib import SMTPException

from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.core.cache import cache
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, UpdateView, ListView, DetailView, DeleteView
from .models import Mailing, RecipientMailing, Message, MailingAttempt

from .forms import RecipientMailingForm, MessageForm, MailingForm


class RecipientListView(LoginRequiredMixin, ListView):
    model = RecipientMailing
    template_name = "mailing_service/recipients_mailing.html"
    success_url = reverse_lazy("mailing_service:home_views")
    context_object_name = "recipients_mailing"

    def get_queryset(self):
        if self.request.user.has_perm("recipientmailing.can_view_all_recipient_lists"):
            return RecipientMailing.objects.all()
        return RecipientMailing.objects.filter(created_by=self.request.user)


class RecipientCreateView(LoginRequiredMixin, CreateView):
    form_class = RecipientMailingForm
    template_name = "mailing_service/form_create_recipient_mailing.html"
    success_url = reverse_lazy("mailing_service:home_views")

    def form_valid(self, form):
        recipient = form.save(commit=False)
        recipient.created_by = self.request.user
        recipient.save()

        return super().form_valid(form)


class RecipientUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = RecipientMailing
    form_class = RecipientMailingForm
    template_name = "mailing_service/form_create_recipient_mailing.html"
    permission_required = "auth_users.change_receiver"

    def has_permission(self):
        obj = self.get_object()
        return obj.created_by == self.request.user

    def get_success_url(self):
        return reverse_lazy("mailing_service:recipients_mailing_views")


class RecipientDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = RecipientMailing
    template_name = "mailing_service/delete_recipient.html"
    success_url = reverse_lazy("mailing_service:home_views")
    context_object_name = "recipient"

    def has_permission(self):
        obj = self.get_object()
        return obj.created_by == self.request.user


class RecipientDetailView(LoginRequiredMixin, DetailView):
    model = RecipientMailing
    template_name = "mailing_service/detail_recipient.html"
    context_object_name = "recipient"
    success_url = reverse_lazy("mailing_service:home_views")


class MessageListView(LoginRequiredMixin, ListView):
    model = Message
    template_name = "mailing_service/messages.html"
    success_url = reverse_lazy("mailing_service:home_views")
    context_object_name = "messages"

    def get_queryset(self):
        queryset = cache.get("message_list")
        if not queryset:
            if self.request.user.has_perm("message.can_view_all_message_lists"):
                queryset = Message.objects.all()
                cache.set("message_list", queryset, 60)
            else:
                queryset = Message.objects.filter(created_by=self.request.user)
                cache.set("message_list", queryset, 60)
        return queryset


class MessageDetailView(LoginRequiredMixin, DetailView):
    model = Message
    template_name = "mailing_service/detail_message.html"
    context_object_name = "message"
    success_url = reverse_lazy("mailing_service:home_views")


class MessageUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Message
    form_class = MessageForm
    template_name = "mailing_service/form_create_message.html"

    def has_permission(self):
        obj = self.get_object()
        return obj.created_by == self.request.user

    def get_success_url(self):
        return reverse_lazy("mailing_service:messages_views")


class MessageDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Message
    template_name = "mailing_service/delete_message.html"
    success_url = reverse_lazy("mailing_service:home_views")
    context_object_name = "message"

    def has_permission(self):
        obj = self.get_object()
        return obj.created_by == self.request.user


class MessageCreateView(LoginRequiredMixin, CreateView):
    form_class = MessageForm
    template_name = "mailing_service/form_create_message.html"
    success_url = reverse_lazy("mailing_service:home_views")

    def form_valid(self, form):
        message = form.save(commit=False)
        message.created_by = self.request.user
        message.save()

        return super().form_valid(form)


class MailingCreateView(LoginRequiredMixin, CreateView):
    form_class = MailingForm
    template_name = "mailing_service/form_create_mailing.html"
    success_url = reverse_lazy("mailing_service:home_views")

    def form_valid(self, form):
        mailing = form.save(commit=False)
        mailing.created_by = self.request.user
        mailing.save()

        return super().form_valid(form)


class MailingDetailView(LoginRequiredMixin, DetailView):
    model = Mailing
    template_name = "mailing_service/detail_mailing.html"
    context_object_name = "mailing"
    success_url = reverse_lazy("mailing_service:home_views")


class MailingUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Mailing
    form_class = MailingForm
    template_name = "mailing_service/form_create_mailing.html"
    permission_required = "auth_users.change_receiver"

    def has_permission(self):
        obj = self.get_object()
        return obj.created_by == self.request.user

    def get_success_url(self):
        return reverse_lazy("mailing_service:mailing_views")


class MailingDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Mailing
    template_name = "mailing_service/delete_mailing.html"
    success_url = reverse_lazy("mailing_service:mailing_views")
    context_object_name = "mailing"

    def has_permission(self):
        obj = self.get_object()
        return obj.created_by == self.request.user


class DisableMailingView(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = "mailing.can_disable_mailing"

    def post(self, request, pk):
        mailing = get_object_or_404(Mailing, id=pk)

        mailing.status = "Создана"
        mailing.save()

        return redirect("mailing_service:mailing_views")


class SendMailView(View):

    def post(self, request, pk):
        mail = get_object_or_404(Mailing, id=pk)
        user = self.request.user

        try:
            mail_sent = send_mail(
                mail.messages.topic_message,
                mail.messages.message,
                "serega94nn@yandex.ru",
                [i.email for i in mail.recipients.all()],
                fail_silently=False,
            )
            if mail.status != "Запущена":
                mail.status = "Запущена"
                mail.save()
            user.total_attempt += 1

        except SMTPException as e:
            mail_attempt = MailingAttempt(status="Не успешно", mail_server_response=e, mailing=mail)
            user.unsuccessful_attempt += 1
            mail_attempt.save()
            user.save()

        else:
            mail_attempt = MailingAttempt(status="Успешно", mail_server_response="Письмо доставлено", mailing=mail)
            user.successful_attempt += 1
            mail_attempt.save()
            user.save()

        return redirect("mailing_service:home_views")


class MailListView(LoginRequiredMixin, ListView):
    model = Mailing
    template_name = "mailing_service/mailing.html"
    success_url = reverse_lazy("mailing_service:home_views")
    context_object_name = "mailing"

    def get_queryset(self):
        # Получаем только активные объекты
        if self.request.user.has_perm("mailing.can_view_all_mailing_lists"):
            return Mailing.objects.all()
        return Mailing.objects.filter(created_by=self.request.user)


class MailingListView(LoginRequiredMixin, ListView):
    model = Mailing
    template_name = "mailing_service/home.html"
    success_url = reverse_lazy("mailing_service:home_views")
    context_object_name = "mailing"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["total_mailings"] = len(Mailing.objects.all())
        context["total_launched_mailings"] = len(Mailing.objects.filter(status="Запущена"))
        context["total_recipients"] = len(RecipientMailing.objects.all())
        return context

    def get_queryset(self):
        # Получаем только активные объекты
        return Mailing.objects.filter(created_by=self.request.user, status="Запущена")


class NotFoundRecipientsView(LoginRequiredMixin, View):
    template_name = "mailing_service/not_found_recipients.html"
