from django import forms

from mailing.models import Mailing, Client, Message


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
    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # определяем список клиентов для рассылки, принадлежащих пользователю
        self.fields['mailing_clients'].queryset = Client.objects.filter(client_owner=user)

        # определяем список сообщений для рассылки, принадлежащих пользователю
        self.fields['mailing_message'].queryset = Message.objects.filter(message_owner=user)

    class Meta:
        """
        Определяет параметры формы
        """
        model = Mailing

        exclude = ('mailing_log', 'mailing_owner')  # выводит в форму все поля, кроме указанных
        widgets = {
            'mailing_time_start': forms.DateTimeInput(
                attrs={'type': 'datetime-local'}
            ),
            'mailing_time_finish': forms.DateTimeInput(
                attrs={'type': 'datetime-local'})
        }


class ClientForm(StyleFormMixin, forms.ModelForm):
    """
     Создает форму для создания клиента
    """

    class Meta:
        """
        Определяет параметры формы
        """
        model = Client

        exclude = ('client_owner',)  # выводит в форму все поля, кроме указанных


class MessageForm(StyleFormMixin, forms.ModelForm):
    """
     Создает форму для создания сообщения
    """

    class Meta:
        """
        Определяет параметры формы
        """
        model = Message

        exclude = ('message_owner',)  # выводит в форму все поля, кроме указанных
