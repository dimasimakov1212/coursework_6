from django.urls import path

from mailing.views import index

# from main.apps import MainConfig
#
# app_name = MainConfig.name

urlpatterns = [
    path('', index, name='home'),

]
