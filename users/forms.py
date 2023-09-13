from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms

from users.models import User


class UserRegisterForm(UserCreationForm):
    """
    Форма регистрации пользователя
    """
    class Meta:
        model = User
        fields = ('email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class UserProfileForm(UserChangeForm):
    """
    Форма профиля пользователя
    """
    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'phone', 'avatar')

    def __init__(self, *args, **kwargs):
        """
        Дополнительные настройки
        """
        super().__init__(*args, **kwargs)

        # Позволяет не выводить в профиле поле пароля
        self.fields['password'].widget = forms.HiddenInput()

        # передаем в шаблон контроль формы
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class ManagerUpdateUserProfileForm(UserChangeForm):
    """
    Форма профиля пользователя для редактирования менеджером
    """

    class Meta:
        model = User
        fields = ('is_active',)

    def __init__(self, *args, **kwargs):
        """
        Дополнительные настройки
        """
        super().__init__(*args, **kwargs)

        # Позволяет не выводить в профиле поле пароля
        self.fields['password'].widget = forms.HiddenInput()

        # передаем в шаблон контроль формы
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
