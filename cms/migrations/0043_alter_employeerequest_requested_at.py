# Generated by Django 4.0.4 on 2022-04-27 11:05

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0042_employeerequest_requested_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employeerequest',
            name='requested_at',
            field=models.DateTimeField(default=datetime.datetime(2022, 4, 27, 11, 5, 21, 387749, tzinfo=utc)),
        ),
    ]
