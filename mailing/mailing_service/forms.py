from datetime import datetime

from django import forms

from .models import RecipientMailing, Message, Mailing


class RecipientMailingForm(forms.ModelForm):
    email = forms.EmailField(
        label="Email", widget=forms.EmailInput(attrs={"class": "form-control", "style": "width: 400px"})
    )
    full_name = forms.CharField(
        label="ФИО", widget=forms.TextInput(attrs={"class": "form-control", "style": "width: 400px"})
    )
    comment = forms.CharField(
        label="Комментарий", widget=forms.TextInput(attrs={"class": "form-control", "style": "width: 400px"})
    )

    class Meta:
        model = RecipientMailing
        fields = ["email", "full_name", "comment"]


class MessageForm(forms.ModelForm):
    topic_message = forms.CharField(
        label="Тема письма", widget=forms.TextInput(attrs={"class": "form-control", "style": "width: 400px"})
    )
    message = forms.CharField(
        label="Содержание письма", widget=forms.Textarea(attrs={"class": "form-control", "style": "width: 400px"})
    )

    class Meta:
        model = Message
        fields = ["topic_message", "message"]


class MailingForm(forms.ModelForm):
    start_mailing = forms.DateTimeField(
        label="Время начала рассылки",
        input_formats=["%d/%m/%Y %H:%M"],
        widget=forms.DateTimeInput(format="%d/%m/%Y %H:%M", attrs={"class": "form-control", "type": "datetime-local"}),
    )
    end_mailing = forms.DateTimeField(
        label="Время окончания рассылки",
        input_formats=["%d/%m/%Y %H:%M"],
        widget=forms.DateTimeInput(format="%d/%m/%Y %H:%M", attrs={"class": "form-control", "type": "datetime-local"}),
    )
    messages = forms.ModelChoiceField(
        label="Письмо",
        queryset=Message.objects.all(),
        widget=forms.Select(attrs={"class": "form-select", "style": "width: 200px"}),
    )
    recipients = forms.ModelMultipleChoiceField(
        label="Получатели",
        queryset=RecipientMailing.objects.all(),
        widget=forms.SelectMultiple(attrs={"class": "form-select"}),
    )

    class Meta:
        model = Mailing
        fields = ["start_mailing", "end_mailing", "messages", "recipients"]

    def clean_status(self):
        """Валидация цены товара"""
        status = self.cleaned_data.get("status")
        end_mailing = self.cleaned_data.get("end_mailing")
        if end_mailing and end_mailing < datetime.now():
            status = "Завершена"

        return status
