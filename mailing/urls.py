from django.urls import path

from mailing.views import index

from mailing.apps import MailingConfig

app_name = MailingConfig.name

urlpatterns = [
    path('', index, name='home'),

]
