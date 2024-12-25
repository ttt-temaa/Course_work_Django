from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.exceptions import PermissionDenied

from django.urls import reverse_lazy

from django.views.generic import CreateView, DeleteView, DetailView, ListView, TemplateView, UpdateView

from mailing.forms import MailingForm, MessageForm, RecipientForm
from mailing.models import Mailing, MailingAttempt, Message, RecipientMailing


class IndexView(TemplateView):
    template_name = "mailing/index.html"

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data["title"] = "Главная"
        context_data["count_mailing"] = len(Mailing.objects.all())
        active_mailings_count = Mailing.objects.filter(status="Запущена").count()
        context_data["active_mailings_count"] = active_mailings_count
        unique_clients_count = RecipientMailing.objects.distinct().count()
        context_data["unique_clients_count"] = unique_clients_count
        return context_data


class MailingListView(LoginRequiredMixin, ListView):
    model = Mailing

    def get_queryset(self, *args, **kwargs):
        if self.request.user.is_superuser or self.request.user.groups.filter(name="Менеджеры").exists():
            return super().get_queryset()
        elif self.request.user.groups.filter(name="Пользователи").exists():
            return super().get_queryset().filter(owner=self.request.user)
        raise PermissionDenied


class MailingDetailView(LoginRequiredMixin, DetailView):
    model = Mailing
    form_class = MailingForm

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if self.request.user.groups.filter(name="Менеджеры") or self.request.user.is_superuser:
            return self.object
        if self.object.owner != self.request.user and not self.request.user.is_superuser:
            raise PermissionDenied
        return self.object


class MailingCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Mailing
    form_class = MailingForm
    success_url = reverse_lazy("mailing:mailing_list")

    def form_valid(self, form):
        recipient = form.save()
        recipient.owner = self.request.user
        recipient.save()
        return super().form_valid(form)

    def test_func(self):
        return self.request.user.groups.filter(name="Пользователи").exists() or self.request.user.is_superuser


class MailingUpdateView(LoginRequiredMixin, UpdateView):
    model = Mailing
    form_class = MailingForm
    success_url = reverse_lazy("mailing:mailing_list")

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if self.object.owner != self.request.user and not self.request.user.is_superuser:
            raise PermissionDenied
        return self.object


class MailingDeleteView(LoginRequiredMixin, DeleteView):
    model = Mailing
    success_url = reverse_lazy("mailing:mailing_list")

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if self.object.owner != self.request.user and not self.request.user.is_superuser:
            raise PermissionDenied
        return self.object


class RecipientMailingListView(ListView):
    model = RecipientMailing

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data["title"] = "Получатели"
        return context_data

    def get_queryset(self, *args, **kwargs):
        if self.request.user.is_superuser or self.request.user.groups.filter(name="Менеджеры"):
            return super().get_queryset()
        elif self.request.user.groups.filter(name="Пользователи"):
            return super().get_queryset().filter(owner=self.request.user)
        raise PermissionDenied


class RecipientMailingDetailView(LoginRequiredMixin, DetailView):
    model = RecipientMailing
    form_class = RecipientForm

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if self.request.user.is_superuser or self.request.user.groups.filter(name="Менеджеры"):
            return self.object
        if self.object.owner != self.request.user and not self.request.user.is_superuser:
            raise PermissionDenied
        return self.object


class RecipientMailingCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = RecipientMailing
    form_class = RecipientForm
    success_url = reverse_lazy("mailing:recipientmailing_list")

    def form_valid(self, form):
        recipient = form.save()
        recipient.owner = self.request.user
        recipient.save()
        return super().form_valid(form)

    def test_func(self):
        return self.request.user.groups.filter(name="Пользователи").exists() or self.request.user.is_superuser


class RecipientMailingUpdateView(LoginRequiredMixin, UpdateView):
    model = RecipientMailing
    form_class = RecipientForm
    success_url = reverse_lazy("mailing:recipientmailing_list")

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if self.object.owner != self.request.user and not self.request.user.is_superuser:
            raise PermissionDenied
        return self.object


class RecipientMailingDeleteView(LoginRequiredMixin, DeleteView):
    model = RecipientMailing
    success_url = reverse_lazy("mailing:recipientmailing_list")

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if self.object.owner != self.request.user and not self.request.user.is_superuser:
            raise PermissionDenied
        return self.object


class MessageListView(ListView):
    model = Message

    def get_queryset(self, *args, **kwargs):
        if self.request.user.is_superuser:
            return super().get_queryset()
        else:
            raise PermissionDenied


class MessageDetailView(LoginRequiredMixin, DetailView):
    model = Message
    form_class = MessageForm

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if not self.request.user.is_superuser:
            raise PermissionDenied
        return self.object


class MessageCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Message
    form_class = MessageForm
    success_url = reverse_lazy("mailing:message_list")

    def form_valid(self, form):
        recipient = form.save()
        recipient.owner = self.request.user
        recipient.save()
        return super().form_valid(form)

    def test_func(self):
        return self.request.user.is_superuser


class MessageUpdateView(LoginRequiredMixin, UpdateView):
    model = Message
    form_class = MessageForm
    success_url = reverse_lazy("mailing:message_list")

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if not self.request.user.is_superuser:
            raise PermissionDenied
        return self.object


class MessageDeleteView(LoginRequiredMixin, DeleteView):
    model = Message
    success_url = reverse_lazy("mailing:message_list")

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if not self.request.user.is_superuser:
            raise PermissionDenied
        return self.object


class MailingAttemptCreateView(LoginRequiredMixin, CreateView):
    model = MailingAttempt

    def form_valid(self, form):
        recipient = form.save()
        recipient.owner = self.request.user
        recipient.save()
        return super().form_valid(form)


class MailingAttemptListView(LoginRequiredMixin, ListView):
    model = MailingAttempt

    def get_queryset(self, *args, **kwargs):
        if self.request.user.is_superuser:
            return super().get_queryset()
        elif self.request.user.groups.filter(name="Пользователи").exists():
            return super().get_queryset().filter(owner=self.request.user)
        raise PermissionDenied
