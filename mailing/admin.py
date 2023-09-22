from django.contrib import admin

from mailing.models import Client, Message, Mailing


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    """
    Описывает параметры для вывода таблицы клиентов в админку
    """
    list_display = ('client_email', 'client_first_name', 'client_last_name', 'client_owner',)
    list_filter = ('client_email',)
    search_fields = ('client_email',)


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    """
    Описывает параметры для вывода таблицы клиентов в админку
    """
    list_display = ('message_title',)
    list_filter = ('message_title',)
    search_fields = ('message_title',)


@admin.register(Mailing)
class MailingAdmin(admin.ModelAdmin):
    """
    Описывает параметры для вывода таблицы клиентов в админку
    """
    list_display = ('mailing_title', 'mailing_period', 'mailing_status', 'mailing_owner',)
    list_filter = ('mailing_title',)
    search_fields = ('mailing_title',)
