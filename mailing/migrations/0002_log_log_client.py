# Generated by Django 4.2.5 on 2023-09-23 16:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mailing', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='log',
            name='log_client',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='mailing.client', verbose_name='клиент'),
        ),
    ]