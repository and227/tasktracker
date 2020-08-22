# Generated by Django 3.1 on 2020-08-22 18:44

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tasktracker', '0024_auto_20200820_2127'),
    ]

    operations = [
        migrations.AlterField(
            model_name='statistic',
            name='date_point',
            field=models.DateField(default=datetime.datetime(2020, 8, 22, 18, 44, 15, 159845)),
        ),
        migrations.AlterField(
            model_name='task',
            name='task_begin',
            field=models.DateTimeField(default=datetime.datetime(2020, 8, 22, 18, 44, 15, 159357)),
        ),
        migrations.AlterField(
            model_name='task',
            name='task_end',
            field=models.DateTimeField(default=datetime.datetime(2020, 8, 22, 18, 44, 15, 159374)),
        ),
        migrations.AlterField(
            model_name='task',
            name='template',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='template_tasks', to='tasktracker.template'),
        ),
    ]
