import datetime
from random import sample

import pytz
from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.cache import cache
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy, reverse

from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView

from blog.models import Blog
from mailing.forms import MailingForm, ClientForm, MessageForm
from mailing.models import Mailing, Client, Message, Log
from mailing.services import sending_email


class MailingListView(ListView):
    """
    Выводит информаццию о рассылках пользователя
    """
    model = Mailing
    template_name = 'mailing/mailing_list.html'

    def get_queryset(self, *args, **kwargs):
        """
        Выводит в список только рассылки для конкретного пользователя
        """
        queryset = super().get_queryset(*args, **kwargs)

        try:
            user = self.request.user

            # если суперпользователь или менеджер, выводит все рассылки
            if user.is_superuser or user.groups.filter(name='manager'):
                return queryset

            # если пользователь, выводит все рассылки
            else:
                queryset = queryset.filter(mailing_owner=user)
                return queryset

        except TypeError:
            pass

    def get_context_data(self, **kwargs):
        """
        Выводит контекстную информацию в шаблон
        """
        context = super(MailingListView, self).get_context_data(**kwargs)

        context['title'] = 'Рассылки'
        context['title_2'] = 'мои рассылки'
        context['title_3'] = ('(Перед созданием рассылки необходимо занести клиента и создать сообщение. '
                              'Кнопка отправить рассылки сейчас позволяет запустить рассылки вне расписания)')

        return context


class MailingCreateView(LoginRequiredMixin, CreateView):
    """
    Выводит форму создания рассылки
    """
    model = Mailing
    form_class = MailingForm

    success_url = reverse_lazy('mailing:mailing_list')

    def form_valid(self, form):
        """
        Проверяем данные на правильность заполнения
        """

        user = self.request.user
        self.object = form.save()
        self.object.mailing_owner = user
        self.object.save()

        return super().form_valid(form)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs


class MailingDetailView(DetailView):
    """
    Выводит информаццию об одной рассылке
    """
    model = Mailing

    def get_context_data(self, **kwargs):
        """
        Выводит контекстную информацию в шаблон
        """
        context = super(MailingDetailView, self).get_context_data(**kwargs)

        context['title'] = 'Рассылки'
        context['title_2'] = 'информация о рассылке'

        return context


class MailingUpdateView(UpdateView):
    """
    Выводит форму редактирования рассылки
    """
    model = Mailing
    form_class = MailingForm

    success_url = reverse_lazy('mailing:mailing_list')

    def form_valid(self, form):
        """
        Проверяем данные на правильность заполнения
        """
        self.object = form.save()
        self.object.save()

        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        """
        Выводит контекстную информацию в шаблон
        """
        context = super(MailingUpdateView, self).get_context_data(**kwargs)
        context['title'] = 'Рассылки'
        context['title_2'] = 'Редактирование рассылки'
        return context

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs


class MailingDeleteView(DeleteView):
    """
    Выводит форму удаления рассылки
    """
    model = Mailing

    success_url = reverse_lazy('mailing:mailing_list')

    def get_context_data(self, **kwargs):
        """
        Выводит контекстную информацию в шаблон
        """
        context = super(MailingDeleteView, self).get_context_data(**kwargs)
        context['title'] = 'Рассылки'
        context['title_2'] = 'Удаление рассылки'
        return context


class ClientListView(ListView):
    """
    Выводит информаццию о клиентах пользователя
    """
    model = Client
    template_name = 'mailing/client_list.html'

    def get_queryset(self, *args, **kwargs):
        """
        Выводит в список только клиентов конкретного пользователя
        """
        queryset = super().get_queryset(*args, **kwargs)

        queryset = queryset.filter(client_owner=self.request.user)

        return queryset

    def get_context_data(self, **kwargs):
        """
        Выводит контекстную информацию в шаблон
        """
        context = super(ClientListView, self).get_context_data(**kwargs)

        context['title'] = 'Клиенты'
        context['title_2'] = 'мои клиенты для рассылок'

        return context


class ClientCreateView(LoginRequiredMixin, CreateView):
    """
    Выводит форму создания клиента
    """
    model = Client
    form_class = ClientForm

    success_url = reverse_lazy('mailing:client_list')

    def form_valid(self, form):
        """
        Проверяем данные на правильность заполнения
        """
        self.object = form.save()
        self.object.client_owner = self.request.user
        self.object.save()

        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        """
        Выводит контекстную информацию в шаблон
        """
        context = super(ClientCreateView, self).get_context_data(**kwargs)
        context['title'] = 'Клиенты'
        context['title_2'] = 'Создание клиента'
        return context


class ClientUpdateView(LoginRequiredMixin, UpdateView):
    """
    Выводит форму редактирования клиента
    """
    model = Client
    form_class = ClientForm

    success_url = reverse_lazy('mailing:client_list')

    def form_valid(self, form):
        """
        Проверяем данные на правильность заполнения
        """
        self.object = form.save()
        self.object.save()

        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        """
        Выводит контекстную информацию в шаблон
        """
        context = super(ClientUpdateView, self).get_context_data(**kwargs)
        context['title'] = 'Клиенты'
        context['title_2'] = 'Редактирование клиента'
        return context


class ClientDeleteView(DeleteView):
    """
    Выводит форму удаления клиента
    """
    model = Client

    success_url = reverse_lazy('mailing:client_list')

    def get_context_data(self, **kwargs):
        """
        Выводит контекстную информацию в шаблон
        """
        context = super(ClientDeleteView, self).get_context_data(**kwargs)
        context['title'] = 'Клиенты'
        context['title_2'] = 'Удаление клиента'
        return context


class MessageListView(LoginRequiredMixin, ListView):
    """
    Выводит информаццию о сообщениях пользователя для рассылок
    """
    model = Message
    template_name = 'mailing/message_list.html'

    def get_queryset(self, *args, **kwargs):
        """
        Выводит в список только сообщения конкретного пользователя
        """
        queryset = super().get_queryset(*args, **kwargs)

        queryset = queryset.filter(message_owner=self.request.user)

        return queryset

    def get_context_data(self, **kwargs):
        """
        Выводит контекстную информацию в шаблон
        """
        context = super(MessageListView, self).get_context_data(**kwargs)

        context['title'] = 'Сообщения'
        context['title_2'] = 'мои сообщения для рассылок'

        return context


class MessageCreateView(LoginRequiredMixin, CreateView):
    """
    Выводит форму создания клиента
    """
    model = Message
    form_class = MessageForm

    success_url = reverse_lazy('mailing:message_list')

    def form_valid(self, form):
        """
        Проверяем данные на правильность заполнения
        """
        self.object = form.save()
        self.object.message_owner = self.request.user
        self.object.save()

        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        """
        Выводит контекстную информацию в шаблон
        """
        context = super(MessageCreateView, self).get_context_data(**kwargs)
        context['title'] = 'Сообщения'
        context['title_2'] = 'Создание сообщения'
        return context


class MessageUpdateView(LoginRequiredMixin, UpdateView):
    """
    Выводит форму редактирования сообщения
    """
    model = Message
    form_class = MessageForm

    success_url = reverse_lazy('mailing:message_list')

    def form_valid(self, form):
        """
        Проверяем данные на правильность заполнения
        """
        self.object = form.save()
        self.object.save()

        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        """
        Выводит контекстную информацию в шаблон
        """
        context = super(MessageUpdateView, self).get_context_data(**kwargs)
        context['title'] = 'Сообщения'
        context['title_2'] = 'Редактирование сообщения'
        return context


class MessageDeleteView(LoginRequiredMixin, DeleteView):
    """
    Выводит форму удаления сообщения
    """
    model = Message

    success_url = reverse_lazy('mailing:message_list')

    def get_context_data(self, **kwargs):
        """
        Выводит контекстную информацию в шаблон
        """
        context = super(MessageDeleteView, self).get_context_data(**kwargs)
        context['title'] = 'Сообщения'
        context['title_2'] = 'Удаление сообщения'
        return context


def send_mailing_to_clients(request):
    """
    Функция отправки рассылок клиентам
    """

    date_time_now = datetime.datetime.now()  # получаем текущие дату и время
    user = request.user
    mailings = Mailing.objects.filter(mailing_owner=user)  # получаем рассылки пользователя

    desired_timezone = pytz.timezone('Europe/Moscow')

    for mailing in mailings:
        time_start = mailing.mailing_time_start.astimezone(desired_timezone)
        time_now = date_time_now.astimezone(desired_timezone)
        time_finish = mailing.mailing_time_finish.astimezone(desired_timezone)

        if mailing.mailing_status == 'рассылается':  # проверяем статус рассылки, если 'рассылается', то происходит отправка

            if time_start < time_now < time_finish:

                for client in mailing.mailing_clients.all():

                    sending_email(mailing, client)  # функция отправки письма
            elif time_now > time_finish:
                mailing.mailing_status = mailing.STATUS_STOPPED
                mailing.save()

    return redirect(reverse('mailing:mailing_list'))


def mailing_logs(request, pk):
    """
    Выводит список логов рассылки
    :param request:
    :param pk: id рассылки
    :return:
    """
    # mailing = get_object_or_404(Mailing, pk=pk)
    # logs = Log.objects.filter(log_mailing=mailing).order_by('-log_date_time')[:10]
    #
    # if (mailing.mailing_owner == request.user or request.user.is_superuser
    #         or request.user.groups.filter(name='manager').exists()):
    #     context = {
    #         'title': 'Логи',
    #         'title_2': 'логи ваших рассылок',
    #         'title_3': '(выводится список из 10 последних логов рассылки)',
    #         'logs': logs,
    #     }
    #     return render(request, 'mailing/log_list.html', context)
    # else:
    #     return redirect("mailing:mailing_list")

# ----------------- вариант с кэшированием -----------------------------------

    mailing = get_object_or_404(Mailing, pk=pk)

    if settings.CACHE_ENABLED:  # если включено кэширование
        key = 'logs_list'  # ключ, по которому получаем список пользователей
        logs = cache.get(key)  # получаем данные из кэша

        if logs is None:  # проверяем кэш, если пусто, получаем данные из БД
            logs = Log.objects.filter(log_mailing=mailing).order_by('-log_date_time')[:10]

            cache.set(key, logs)  # записываем полученные данные в кэш

    else:  # если кэширование не включено
        logs = Log.objects.filter(log_mailing=mailing).order_by('-log_date_time')[:10]  # получаем данные из БД

    if (mailing.mailing_owner == request.user or request.user.is_superuser
            or request.user.groups.filter(name='manager').exists()):
        context = {
            'title': 'Логи',
            'title_2': 'логи ваших рассылок',
            'title_3': '(выводится список из 10 последних логов рассылки)',
            'logs': logs,
        }
        return render(request, 'mailing/log_list.html', context)
    else:
        return redirect("mailing:mailing_list")

# ---------------------------- конец -----------------------------------------


def main_page_view(request):
    """
    Выводит на главную страницу
    :return:
    """
    # вроде как нежелательный вариант получения трех случайных статей
    # blog_list = Blog.objects.filter(blog_is_active=True).order_by('?')[:3]

    blogs = Blog.objects.filter(blog_is_active=True)  # Получаем все опубликованные статьи
    if len(blogs) >= 3:
        blog_list = sample(list(blogs), 3)  # Получаем 3 случайных статьи
    else:
        blog_list = blogs

    mailings_count = Mailing.objects.count()  # получаем количество рассылок всего

    # определяем количество рассылок, которые рассылаются
    mailings_is_sending = Mailing.objects.filter(mailing_status='рассылается').count()

    clients_count = Client.objects.count()  # получаем количество клиентов для рассылок

    context = {
        'title': 'Главная',
        'title_2': 'сервис создания рассылок',
        'blog_list': blog_list,
        'mailings_count': mailings_count,
        'mailings_is_sending': mailings_is_sending,
        'clients_count': clients_count
    }
    return render(request, 'mailing/base.html', context)
