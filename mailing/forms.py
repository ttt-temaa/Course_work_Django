from django.forms import BooleanField, ImageField, ModelForm
from django.urls import reverse_lazy

from mailing.models import Mailing, Message, RecipientMailing


class StyleFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for fild_name, fild in self.fields.items():
            if isinstance(fild, BooleanField):
                fild.widget.attrs["class"] = "form-check-input"
            elif isinstance(fild, ImageField):
                fild.widget.attrs["class"] = "form-control-file"
            else:
                fild.widget.attrs["class"] = "form-control"


class MailingForm(StyleFormMixin, ModelForm):
    class Meta:
        model = Mailing
        fields = "__all__"
        success_url = reverse_lazy("mailing:mailing_list")


class RecipientForm(StyleFormMixin, ModelForm):
    class Meta:
        model = RecipientMailing
        fields = "__all__"
        success_url = reverse_lazy("mailing:recipientmailing_list")


class MessageForm(StyleFormMixin, ModelForm):
    class Meta:
        model = Message
        fields = "__all__"
        success_url = reverse_lazy("mailing:message_list")
