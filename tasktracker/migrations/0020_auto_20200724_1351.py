# Generated by Django 3.0.7 on 2020-07-24 13:51

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasktracker', '0019_auto_20200724_1350'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='task',
            name='task_type',
        ),
        migrations.AlterField(
            model_name='statistic',
            name='date_point',
            field=models.DateField(default=datetime.datetime(2020, 7, 24, 13, 51, 11, 664037)),
        ),
        migrations.AlterField(
            model_name='task',
            name='task_begin',
            field=models.DateTimeField(default=datetime.datetime(2020, 7, 24, 13, 51, 11, 661803)),
        ),
        migrations.AlterField(
            model_name='task',
            name='task_end',
            field=models.DateTimeField(default=datetime.datetime(2020, 7, 24, 13, 51, 11, 661863)),
        ),
    ]