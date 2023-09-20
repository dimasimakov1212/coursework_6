from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from mailing.forms import MailingForm, ClientForm
from mailing.models import Mailing, Client, Message


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

# --------------------- рабочая версия ---------------------------
    def get_context_data(self, **kwargs):
        """
        Выводит контекстную информацию в шаблон
        """
        context = super(MailingListView, self).get_context_data(**kwargs)

        context['title'] = 'Рассылки'
        context['title_2'] = 'ваши рассылки'

        return context
# # ----------------------------------------------------------------


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
        context['title_2'] = 'ваши клиенты для рассылок'

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
        context['title_2'] = 'ваши сообщения для рассылок'

        return context
