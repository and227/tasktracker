# Generated by Django 3.0.7 on 2020-07-21 06:14

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasktracker', '0009_auto_20200718_1755'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='active_intervals',
            field=models.CharField(db_index=True, default=None, max_length=32),
        ),
        migrations.AddField(
            model_name='task',
            name='exclude_selected',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='task',
            name='template_counter',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='task',
            name='task_begin',
            field=models.DateTimeField(default=datetime.datetime(2020, 7, 21, 6, 14, 15, 987229)),
        ),
        migrations.AlterField(
            model_name='task',
            name='task_end',
            field=models.DateTimeField(default=datetime.datetime(2020, 7, 21, 6, 14, 15, 987288)),
        ),
    ]