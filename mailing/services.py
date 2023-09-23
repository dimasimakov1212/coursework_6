from django.core.mail import send_mail

from config import settings


def sending_email(subject, message, email):
    """
    Функция отправки email
    :param email: почта клиента
    :param message: текст рассылки
    :param subject: тема рассылки
    :return:
    """
    send_mail(
        subject=f'{subject}',
        message=f'{message}',
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[f'{email}'],
        fail_silently=False
    )
