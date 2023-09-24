from datetime import datetime
from smtplib import SMTPException

from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views import View
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView

from mailing.forms import MailingForm, ClientForm, MessageForm
from mailing.models import Mailing, Client, Message, Log
from mailing.services import sending_email


class MainPageView(ListView):
    """
    Стартовая страница
    """
    model = Mailing
    template_name = 'mailing/base.html'

    def get_context_data(self, **kwargs):
        """
        Выводит контекстную информацию в шаблон
        """
        context = super(MainPageView, self).get_context_data(**kwargs)

        context['title'] = 'Главная'
        context['title_2'] = 'сервис создания рассылок'

        return context


class MailingListView(ListView):
    """
    Выводит информаццию о рассылках пользователя
    """
    model = Mailing
    template_name = 'mailing/mailing_list.html'

    def get_queryset(self, *args, **kwargs):
        """
        Выводит в список только рассылки конкретного пользователя
        """
        queryset = super().get_queryset(*args, **kwargs)

        try:
            user = self.request.user

            if user.is_superuser or user.groups.filter(name='manager'):
                return queryset

            else:
                queryset = queryset.filter(mailing_owner=user)

        except TypeError:
            pass

        return queryset

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


class MailingCreateView(CreateView):
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
        # formset = self.get_context_data()['formset']
        user = self.request.user
        self.object = form.save()
        self.object.mailing_owner = user
        self.object.save()

        # if formset.is_valid():
        #     formset.instance = self.object
        #     formset.save()

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


class ClientCreateView(CreateView):
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


class ClientUpdateView(UpdateView):
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


class MessageListView(ListView):
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


class MessageCreateView(CreateView):
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


class MessageUpdateView(UpdateView):
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


class MessageDeleteView(DeleteView):
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

    user = request.user
    mailings = Mailing.objects.filter(mailing_owner=user)  # получаем рассылки пользователя

    for mailing in mailings:
        if mailing.mailing_status == 'рассылается':  # проверяем статус рассылки, если 'рассылается', то происходит отправка

            for client in mailing.mailing_clients.all():

                sending_email(mailing, client)  # функция отправки письма

    return redirect(reverse('mailing:mailing_list'))


def mailing_logs(request, pk):
    """
    Выводит список логов рассылки
    :param request:
    :param pk: id рассылки
    :return:
    """
    mailing = get_object_or_404(Mailing, pk=pk)
    logs = Log.objects.filter(log_mailing=mailing).order_by('-log_date_time')[:10]

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
