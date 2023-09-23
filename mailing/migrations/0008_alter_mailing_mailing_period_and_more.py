# Generated by Django 4.2.5 on 2023-09-23 12:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mailing', '0007_alter_mailing_mailing_log'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mailing',
            name='mailing_period',
            field=models.CharField(choices=[('ежедневно', 'ежедневно'), ('еженедельно', 'еженедельно'), ('ежемесячно', 'ежемесячно')], max_length=20, verbose_name='периодичность'),
        ),
        migrations.AlterField(
            model_name='mailing',
            name='mailing_status',
            field=models.CharField(choices=[('создано', 'создано'), ('рассылается', 'рассылается'), ('остановлено', 'остановлено')], default='создано', max_length=20, verbose_name='статус'),
        ),
    ]