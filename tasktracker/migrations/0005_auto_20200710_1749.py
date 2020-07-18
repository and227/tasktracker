# Generated by Django 3.0.7 on 2020-07-10 17:49

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('tasktracker', '0004_auto_20200710_1744'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='lost_time',
            field=models.TimeField(default='17:49'),
        ),
        migrations.AlterField(
            model_name='task',
            name='task_begin',
            field=models.DateTimeField(default=datetime.datetime(2020, 7, 10, 17, 49, 3, 40879, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='task',
            name='task_end',
            field=models.DateTimeField(default=datetime.datetime(2020, 7, 10, 17, 49, 3, 40904, tzinfo=utc)),
        ),
    ]