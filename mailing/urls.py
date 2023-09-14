from django.urls import path

from mailing.views import index, MailingListView, MailingCreateView

from mailing.apps import MailingConfig

app_name = MailingConfig.name

urlpatterns = [
    path('', index, name='home'),
    path('mailing_list', MailingListView.as_view(), name='mailing_list'),
    path('create_mailing/', MailingCreateView.as_view(), name='create_mailing'),
]
