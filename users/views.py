from django.contrib.auth import login
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.views import PasswordResetDoneView
from django.core.cache import cache
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.views import View
from django.views.generic import CreateView, TemplateView, UpdateView, ListView, DetailView

from config import settings
from users.forms import UserRegisterForm, UserProfileForm, ManagerUpdateUserProfileForm
from users.models import User


class RegisterView(CreateView):
    """
    Регистрация нового пользователя и его валидация через письмо на email пользователя
    """
    form_class = UserRegisterForm
    template_name = "users/register.html"
    success_url = reverse_lazy('mailing:home')

    def form_valid(self, form):
        user = form.save()
        user.is_active = False
        user.save()

        # формируем токен и ссылку для подтверждения регистрации
        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        activation_url = reverse_lazy('users:confirm_email', kwargs={'uidb64': uid, 'token': token})

        current_site = '127.0.0.1:8000'

        send_mail(
            subject='Регистрация на платформе',
            message=f"Завершите регистрацию, перейдя по ссылке: http://{current_site}{activation_url}",
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[user.email]
        )
        return redirect('users:email_confirmation_sent')


class UserConfirmEmailView(View):
    """
    Подтверждение пользователем регистрации
    """
    def get(self, request, uidb64, token):
        try:
            uid = urlsafe_base64_decode(uidb64)
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            login(request, user)
            return redirect('users:email_confirmed')
        else:
            return redirect('users:email_confirmation_failed')


class UserConfirmationSentView(PasswordResetDoneView):
    """
    Выводит информацию об отправке на почту подтверждения регистрации
    """
    template_name = "users/registration_sent_done.html"


class UserConfirmedView(TemplateView):
    """
    Выводит информацию об успешной регистрации пользователя
    """
    template_name = 'users/registration_confirmed.html'


class UserConfirmationFailView(View):
    """
    Выводит информацию о невозможности зарегистрировать пользователя
    """
    template_name = 'users/email_confirmation_failed.html'


class ProfileView(UpdateView):
    """
    Контроллер профиля пользователя
    """
    model = User
    form_class = UserProfileForm
    success_url = reverse_lazy('users:profile')

    def get_object(self, queryset=None):
        """
        Позволяет делать необязательным передачу pk объекта
        """
        return self.request.user

    # def get_form_class(self):
    #     # product = self.get_object()
    #     user = self.request.user
    #
    #     if user.is_staff:  # проверяем права доступа
    #         return ManagerUpdateUserProfileForm  # если менеджер, то выводится отдельная форма
    #
    #     else:
    #         return UserProfileForm

    def get_context_data(self, **kwargs):
        """
        Выводит контекстную информацию в шаблон
        """
        context = super(ProfileView, self).get_context_data(**kwargs)

        context['title'] = 'Профиль'
        context['title_2'] = 'редактирование профиля пользователя'

        return context


class UserListView(PermissionRequiredMixin, ListView):
    """
    Выводит информаццию о пользователях
    """

    model = User
    permission_required = 'users.view_user'
    template_name = 'users/user_list.html'

    def get_context_data(self, **kwargs):
        """
        Выводит контекстную информацию в шаблон
        """
        context = super(UserListView, self).get_context_data(**kwargs)

        if settings.CACHE_ENABLED:  # если включено кэширование
            key = 'users_list'  # ключ, по которому получаем список пользователей
            users_list = cache.get(key)  # получаем данные из кэша

            if users_list is None:  # проверяем кэш
                users_list = User.objects.all()  # если пусто, получаем данные из БД

                cache.set(key, users_list)  # записываем полученные данные в кэш

        else:  # если кэширование не включено
            users_list = User.objects.all()  # получаем данные из БД

        context['object_list'] = users_list  # передаем в контекст список пользователей

        context['title'] = 'Пользователи'
        context['title_2'] = 'пользователи сервиса рассылок'

        return context


class UserDetailView(DetailView):
    """
    Выводит информаццию об одной рассылке
    """
    model = User

    def get_context_data(self, **kwargs):
        """
        Выводит контекстную информацию в шаблон
        """
        context = super(UserDetailView, self).get_context_data(**kwargs)

        context['title'] = 'Пользователь'
        context['title_2'] = 'информация о пользователе сервиса'

        return context
