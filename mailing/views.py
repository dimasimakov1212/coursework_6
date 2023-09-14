from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView

from mailing.forms import MailingForm
from mailing.models import Mailing


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
    Выводит информаццию о последних 6 товарах на главную страницу
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

    # def get_context_data(self, **kwargs):
    #     """
    #     Выводит контекстную информацию в шаблон
    #     """
    #     context_data = super().get_context_data(**kwargs)
    #
    #     VersionFormset = inlineformset_factory(Product, Version, form=VersionForm, extra=1)
    #
    #     if self.request.method == 'POST':
    #         context_data['formset'] = VersionFormset(self.request.POST, instance=self.object)
    #     else:
    #         context_data['formset'] = VersionFormset(instance=self.object)
    #
    #     return context_data

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
