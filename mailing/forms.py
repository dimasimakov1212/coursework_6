from django import forms

from mailing.models import Mailing


class StyleFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field_name != "is_current_version":
                field.widget.attrs['class'] = 'form-control'


class MailingForm(StyleFormMixin, forms.ModelForm):
    """
     Создает форму для создания рассылки
    """

    class Meta:
        """
        Определяет параметры формы
        """
        model = Mailing

        exclude = ('mailing_status', 'mailing_log', 'mailing_owner')  # выводит в форму все поля, кроме указанных
        widgets = {
            'mailing_time': forms.TimeInput(
                attrs={'type': 'time'}
            )
        }
