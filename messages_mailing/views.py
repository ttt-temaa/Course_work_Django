from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms import BaseModelForm
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

from .forms import MessageForm
from .models import Message


# Create your views here.
class MessageListView(LoginRequiredMixin, ListView):
    model = Message
    template_name = "messages/list.html"
    context_object_name = "messagess"

    def get_queryset(self):
        if self.request.user.has_perm("messages.view_all_messages"):
            return Message.objects.all()
        return Message.objects.filter(owner=self.request.user)
class MessageCreateView(LoginRequiredMixin, CreateView):
    model = Message
    form_class = MessageForm
    template_name = "messages/form.html"
    success_url = reverse_lazy("messages")

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class MessageUpdateView(LoginRequiredMixin, UpdateView):
    model = Message
    form_class = MessageForm
    template_name = "messages/form.html"
    success_url = reverse_lazy("messages")

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        return super().form_valid(form)


class MessageDeleteView(LoginRequiredMixin, DeleteView):
    model = Message
    success_url = reverse_lazy("messages")
