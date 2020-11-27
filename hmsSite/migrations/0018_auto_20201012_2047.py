# Generated by Django 3.1 on 2020-10-12 20:47

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hmsSite', '0017_archivedproject'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='email_sent',
            field=models.BooleanField(default=False, verbose_name='is the project sitll relevant'),
        ),
        migrations.AddField(
            model_name='project',
            name='last_reminder',
            field=models.DateField(default=datetime.date.today, verbose_name='date of the previous archive reminder'),
        ),
    ]
