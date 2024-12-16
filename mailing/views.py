from django.conf import settings
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.mail import send_mail
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

from .forms import MailingForm
from .models import Mailing, MailingAttempt


class MailingListView(ListView):
    model = Mailing
    template_name = "mailing/list.html"
    context_object_name = "mailings"

    def get_queryset(self):
        if self.request.user.has_perm("mailings.view_all_mailings"):
            return Mailing.objects.all()
        return Mailing.objects.filter(owner=self.request.user)


class MailingCreateView(LoginRequiredMixin, CreateView):

    form_class = MailingForm
    template_name = "mailing/form.html"
    success_url = reverse_lazy("mailings")

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class MailingUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Mailing
    form_class = MailingForm
    template_name = "mailing/form.html"
    success_url = reverse_lazy("mailings")
    permission_required = "mailing.change_mailing"

    def has_permission(self):
        return super().has_permission() or self.request.user == self.get_object().owner

    def get_queryset(self):
        return Mailing.objects.filter(owner=self.request.user)

    def form_valid(self, form):
        form.instance.status = "CREATED"
        return super().form_valid(form)


class MailingDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Mailing
    success_url = reverse_lazy("mailings")
    permission_required = "mailing.delete_mailing"

    def has_permission(self):
        return super().has_permission() or self.request.user == self.get_object().owner

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "Рассылка успешно удалена!")
        return super().delete(request, *args, **kwargs)


class MailingReportView(LoginRequiredMixin, DetailView):
    model = Mailing
    template_name = "mailing/report.html"
    context_object_name = "mailing"

    def get_queryset(self):
        if self.request.user.has_perm("mailings.view_all_mailings"):
            return Mailing.objects.all()
        return Mailing.objects.filter(owner=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        mailing = self.get_object()
        attempts = MailingAttempt.objects.filter(mailing=mailing)
        context["attempts"] = attempts
        context["success_count"] = attempts.filter(status="SUCCESS").count()
        context["failure_count"] = attempts.filter(status="FAILURE").count()
        return context


class SendMailingView(LoginRequiredMixin, View):

    def post(self, request, pk):
        # Получаем объект рассылки
        mailing = Mailing.objects.get(pk=pk, owner=request.user)
        message = mailing.message
        recipients = mailing.recipients.all()
        response = None

        # Отправляем сообщения каждому получателю
        for recipient in recipients:
            try:
                send_mail(
                    message.subject,
                    message.body,
                    settings.DEFAULT_FROM_EMAIL,
                    [recipient.email],
                )
                MailingAttempt.objects.create(
                    status="SUCCESS", response=f"Успешно отправлено на {recipient.email}", mailing=mailing
                )
            except Exception as e:
                response = f"Письмо не отправлено на {recipient.email}: {e}"
                MailingAttempt.objects.create(status="FAILURE", response=response, mailing=mailing)
        # Отправляем сообщение об успехе и перенаправляем
        if MailingAttempt.objects.filter(mailing=mailing).order_by("-attempt_time").first().status == "SUCCESS":
            messages.success(request, f"Письмо успешно отправлено на {recipient.email}")
        else:
            messages.warning(request, response)
        mailing.status = "FINISHED"
        mailing.save()
        return redirect("mailings")


class MailingStartView(LoginRequiredMixin, View):
    def post(self, request, pk):
        mailing = Mailing.objects.get(pk=pk)
        mailing.status = "STARTED"
        mailing.save()
        return redirect("mailings")


class MailingStopView(LoginRequiredMixin, View):
    def post(self, request, pk):
        mailing = Mailing.objects.get(pk=pk)
        mailing.status = "CREATED"
        mailing.save()
        return redirect("mailings")
