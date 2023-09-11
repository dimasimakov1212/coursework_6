from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView

from users.apps import UsersConfig

app_name = UsersConfig.name

urlpatterns = [
    path('', LoginView.as_view(template_name='users/login.html'), name='login'),
    ]
