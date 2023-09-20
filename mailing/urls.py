from django.urls import path

from mailing.views import MailingListView, MailingCreateView, MainPageView, ClientListView, ClientCreateView, \
    ClientUpdateView, ClientDeleteView

from mailing.apps import MailingConfig

app_name = MailingConfig.name

urlpatterns = [
    path('', MainPageView.as_view(), name='home'),
    path('mailing/', MailingListView.as_view(), name='mailing_list'),
    path('mailing/create_mailing/', MailingCreateView.as_view(), name='create_mailing'),
    path('mailing/clients/', ClientListView.as_view(), name='client_list'),
    path('mailing/clients/create_client/', ClientCreateView.as_view(), name='create_client'),
    path('mailing/clients/edit_client/<int:pk>/', ClientUpdateView.as_view(), name='edit_client'),
    path('mailing/clients/delete_client/<int:pk>/', ClientDeleteView.as_view(), name='delete_client')
]
