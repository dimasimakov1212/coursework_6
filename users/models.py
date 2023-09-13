from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    username = None
    VERSION_CHOICES = ((True, 'Действующий'), (False, 'Заблокирован'))

    email = models.EmailField(unique=True, verbose_name='почта')
    phone = models.CharField(max_length=35, verbose_name='телефон', blank=True, null=True)
    avatar = models.ImageField(upload_to='users/media/', verbose_name='аватар', blank=True, null=True)
    is_active = models.BooleanField(choices=VERSION_CHOICES, default=True, verbose_name='Статус пользователя')

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
