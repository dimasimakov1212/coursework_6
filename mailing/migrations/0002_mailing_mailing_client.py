# Generated by Django 4.2.5 on 2023-09-14 06:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mailing', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='mailing',
            name='mailing_client',
            field=models.ManyToManyField(to='mailing.client', verbose_name='владелец'),
        ),
    ]
