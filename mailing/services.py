from datetime import datetime
from smtplib import SMTPException
import pytz
import datetime

from django.core.mail import send_mail
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse

from config import settings
from mailing.models import Mailing, Log


def sending_email(mailing, client):
    """
    Функция отправки email
    :param client: клиент для рассылки
    :param mailing: рассылка
    :return:
    """
    date_time_now = datetime.datetime.now()  # получаем текущие дату и время

    subject = mailing.mailing_title  # тема письма
    message = mailing.mailing_message.message_text  # текст письма
    email = client.client_email  # почта клиента

    try:
        send_mail(
            subject=f'{subject}',
            message=f'{message}',
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[f'{email}'],
            fail_silently=False
        )

        # записываем логи рассылки
        Log.objects.create(
            log_status=Log.STATUS_TRUE,
            log_date_time=date_time_now,
            log_server_answer='доставлено',
            log_mailing=mailing,
            log_client=client
        )

    except SMTPException as server_answer:

        Log.objects.create(
            log_status=Log.STATUS_FALSE,
            log_date_time=date_time_now,
            log_server_answer=server_answer,
            log_mailing=mailing,
            log_client=client
        )


def send_all_mailings():
    """
    Функция отправки рассылок клиентам
    """

    mailings = Mailing.objects.filter(mailing_status=Mailing.STATUS_SENT)  # получаем рассылки со статусом "рассылается"
    desired_timezone = pytz.timezone('Europe/Moscow')  # устанавливаем часовой пояс
    date_time_now = datetime.datetime.now()  # получаем текущие дату и время

    for mailing in mailings:  # перебираем рассылки

        # преобразуем даты с учетом часового пояса
        time_start = mailing.mailing_time_start.astimezone(desired_timezone)
        time_now = date_time_now.astimezone(desired_timezone)
        time_finish = mailing.mailing_time_finish.astimezone(desired_timezone)

        for client in mailing.mailing_clients.all():  # перебираем клиентов для рассылки

            mailing_log = Log.objects.filter(log_client=client, log_mailing=mailing)  # получаем данные о логах

            # проверяем попадает ли текущая дата в период рассылки
            if time_start < time_now < time_finish:

                if mailing_log.exists():
                    last_try = mailing_log.order_by('-log_date_time').first()  # получаем последний лог рассылки
                    last_try_date = last_try.log_date_time.astimezone(desired_timezone)  # получаем дату рассылки

                    # делаем проверку периодичности рассылок
                    if mailing.PERIOD_DAILY:
                        if (date_time_now.date() - last_try_date.date()).days >= 1:
                            sending_email(mailing, client)  # отправляем письмо с рассылкой
                    elif mailing.PERIOD_WEEKLY:
                        if (date_time_now.date() - last_try_date.date()).days >= 7:
                            sending_email(mailing, client)
                    elif mailing.PERIOD_MONTHLY:
                        if (date_time_now.date() - last_try_date.date()).days >= 30:
                            sending_email(mailing, client)
                else:
                    sending_email(mailing, client)

            # если текущая дата больше даты окончания рассылки, рассылке присваивается статус "остановлено"
            elif time_now > time_finish:
                mailing.mailing_status = mailing.STATUS_STOPPED
                mailing.save()


def toggle_sending(request, pk):
    """
    Меняет статус рассылки на остановлена
    """
    mailing = get_object_or_404(Mailing, pk=pk)
    if mailing.mailing_status == 'рассылается':
        mailing.mailing_status = 'остановлено'

    mailing.save()

    return redirect(reverse('mailing:mailing_list'))
