from django.contrib import admin

from mailing.models import Client


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    """
    Описывает параметры для вывода таблицы клиентов в админку
    """
    list_display = ('client_email', 'client_first_name', 'client_last_name', 'client_owner',)
    list_filter = ('client_email',)
    search_fields = ('client_email',)
