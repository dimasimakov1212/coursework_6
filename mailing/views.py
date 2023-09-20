from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from mailing.forms import MailingForm, ClientForm
from mailing.models import Mailing, Client


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

    # def get_queryset(self):
    #
    #     user = self.request.user
    #
    #     if user.is_authenticated:  # для зарегистрированных пользователей
    #         if user.is_staff or user.is_superuser:  # для работников и суперпользователя
    #             queryset = super().get_queryset().order_by('-pk')[:6]
    #
    #         else:  # для остальных пользователей
    #             queryset = super().get_queryset().filter(
    #                 is_active=True).order_by('-pk')[:6]
    #     else:  # для незарегистрированных пользователей
    #         queryset = super().get_queryset().filter(
    #             is_active=True).order_by('-pk')[:6]
    #     return queryset

    # def get_queryset(self, *args, **kwargs):
    #     """
    #     Выводит в список только товары конкретного пользователя,
    #     либо если пользователь не авторизован - выводит все товары
    #     """
    #     queryset = super().get_queryset(*args, **kwargs)
    #
    #     try:
    #         queryset = queryset.filter(owner=self.request.user)
    #
    #     except TypeError:
    #         queryset = queryset.all().order_by('-pk')[:5]  # выводит последние 5 товаров
    #
    #     return queryset

# --------------------- рабочая версия ---------------------------
    def get_context_data(self, **kwargs):
        """
        Выводит контекстную информацию в шаблон
        """
        context = super(MailingListView, self).get_context_data(**kwargs)

        # for product in context['product_list']:
        #     active_version = Version.objects.filter(product=product, is_active=True).last()
        #     if active_version:
        #         product.active_version_number = active_version.version_number
        #         product.active_version_name = active_version.version_name
        #     else:
        #         product.active_version_number = None
        #         product.active_version_name = None

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
        formset = self.get_context_data()['formset']
        self.object = form.save()
        self.object.owner = self.request.user
        self.object.save()

        if formset.is_valid():
            formset.instance = self.object
            formset.save()

        return super().form_valid(form)


class ClientListView(ListView):
    """
    Выводит информаццию о клиентах пользователя
    """
    model = Client
    template_name = 'mailing/client_list.html'

    def get_queryset(self, *args, **kwargs):
        """
        Выводит в список только товары конкретного пользователя,
        либо если пользователь не авторизован - выводит все товары
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
