from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView

from users.apps import UsersConfig
from users.views import RegisterView, UserConfirmEmailView, UserConfirmationSentView, UserConfirmedView, \
    UserConfirmationFailView, ProfileView

app_name = UsersConfig.name

urlpatterns = [
    path('', LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    path('email_confirmation_sent/', UserConfirmationSentView.as_view(), name='email_confirmation_sent'),
    path('confirm_email/<str:uidb64>/<str:token>/', UserConfirmEmailView.as_view(), name='confirm_email'),
    path('email_confirmed/', UserConfirmedView.as_view(), name='email_confirmed'),
    path('email_confirmation_failed/', UserConfirmationFailView.as_view(), name='email_confirmation_failed'),
    path('profile/', ProfileView.as_view(), name='profile'),
    ]
