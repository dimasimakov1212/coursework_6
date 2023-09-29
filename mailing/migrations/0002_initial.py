# Generated by Django 4.2.5 on 2023-09-29 04:40

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('mailing', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='message_owner',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='владелец'),
        ),
        migrations.AddField(
            model_name='mailing',
            name='mailing_clients',
            field=models.ManyToManyField(to='mailing.client', verbose_name='клиенты'),
        ),
        migrations.AddField(
            model_name='mailing',
            name='mailing_message',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mailing.message', verbose_name='сообщение'),
        ),
        migrations.AddField(
            model_name='mailing',
            name='mailing_owner',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='владелец'),
        ),
        migrations.AddField(
            model_name='log',
            name='log_client',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='mailing.client', verbose_name='клиент'),
        ),
        migrations.AddField(
            model_name='log',
            name='log_mailing',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mailing.mailing', verbose_name='рассылка'),
        ),
        migrations.AddField(
            model_name='client',
            name='client_owner',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='владелец'),
        ),
    ]