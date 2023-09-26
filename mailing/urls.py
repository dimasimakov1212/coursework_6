from django.urls import path
from django.views.decorators.cache import cache_page

from mailing.services import toggle_sending
from mailing.views import MailingListView, MailingCreateView, ClientListView, ClientCreateView, \
    ClientUpdateView, ClientDeleteView, MessageListView, MessageCreateView, MessageUpdateView, MessageDeleteView, \
    MailingDetailView, MailingUpdateView, MailingDeleteView, send_mailing_to_clients, mailing_logs, main_page_view

from mailing.apps import MailingConfig

app_name = MailingConfig.name

urlpatterns = [
    path('', main_page_view, name='home'),
    path('mailing/', MailingListView.as_view(), name='mailing_list'),
    path('mailing/create_mailing/', MailingCreateView.as_view(), name='create_mailing'),
    path('mailing/mailing_detail/<int:pk>/', cache_page(60)(MailingDetailView.as_view()), name='mailing_detail'),
    path('mailing/edit_mailing/<int:pk>/', MailingUpdateView.as_view(), name='edit_mailing'),
    path('mailing/delete_mailing/<int:pk>/', MailingDeleteView.as_view(), name='delete_mailing'),
    path('mailing/clients/', ClientListView.as_view(), name='client_list'),
    path('mailing/clients/create_client/', ClientCreateView.as_view(), name='create_client'),
    path('mailing/clients/edit_client/<int:pk>/', ClientUpdateView.as_view(), name='edit_client'),
    path('mailing/clients/delete_client/<int:pk>/', ClientDeleteView.as_view(), name='delete_client'),
    path('mailing/messages/', MessageListView.as_view(), name='message_list'),
    path('mailing/messages/create_message/', MessageCreateView.as_view(), name='create_message'),
    path('mailing/messages/edit_message/<int:pk>/', MessageUpdateView.as_view(), name='edit_message'),
    path('mailing/messages/delete_message/<int:pk>/', MessageDeleteView.as_view(), name='delete_message'),
    path('mailing/send_mailing/', send_mailing_to_clients, name='send_mailing'),
    path('mailing/logs/<int:pk>/', mailing_logs, name='log_list'),
    path('mailing/sending/<int:pk>/', toggle_sending, name='toggle_sending'),
]
