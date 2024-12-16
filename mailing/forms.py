from django import forms

from .models import Mailing


class MailingForm(forms.ModelForm):
    class Meta:
        model = Mailing
        fields = ["start_time", "end_time", "message", "recipients"]
        widgets = {
            "start_time": forms.DateTimeInput(
                attrs={"class": "form-control", "type": "datetime-local", "placeholder": "Дата и время начала"}
            ),
            "end_time": forms.DateTimeInput(
                attrs={"class": "form-control", "type": "datetime-local", "placeholder": "Дата и время окончания"}
            ),
            "recipients": forms.CheckboxSelectMultiple(
                attrs={
                    "type": "checkbox",
                    "placeholder": "Получатели",
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field_name == "recipients":
                continue
            field.widget.attrs["class"] = "form-control"
            field.widget.attrs["placeholder"] = field.label
            field.widget.attrs["required"] = True
