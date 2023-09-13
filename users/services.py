from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse

from users.models import User


def toggle_activity(request, pk):
    """
    Меняет статус пользователя (действующий или заблокирован)
    """
    user = get_object_or_404(User, pk=pk)
    if user.is_active:
        user.is_active = False
    else:
        user.is_active = True

    user.save()

    return redirect(reverse('users:user_list'))
