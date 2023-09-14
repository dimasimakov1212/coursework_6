from django.urls import path

from mailing.views import index, MailingListView

from mailing.apps import MailingConfig

app_name = MailingConfig.name

urlpatterns = [
    path('', index, name='home'),
    path('mailing_list', MailingListView.as_view(), name='mailing_list'),
]
