from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

from .forms import RecipientForm
from .models import Recipient


class RecipientListView(LoginRequiredMixin, ListView):
    model = Recipient
    template_name = "recipients/list.html"
    context_object_name = "recipients"

    def get_queryset(self):
        if self.request.user.has_perm("recipients.view_all_recipients"):
            return Recipient.objects.all()
        return Recipient.objects.filter(owner=self.request.user)
class RecipientCreateView(LoginRequiredMixin, CreateView):
    form_class = RecipientForm
    template_name = "recipients/form.html"

    success_url = reverse_lazy("recipients")

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class RecipientUpdateView(LoginRequiredMixin, UpdateView):
    model = Recipient
    form_class = RecipientForm
    template_name = "recipients/form.html"
    success_url = reverse_lazy("recipients")

    def form_valid(self, form):
        return super().form_valid(form)


class RecipientDeleteView(LoginRequiredMixin, DeleteView):
    model = Recipient
    success_url = reverse_lazy("recipients")

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "Получатель успешно удалён!")
        return super().delete(request, *args, **kwargs)
