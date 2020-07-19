# Generated by Django 3.0.7 on 2020-07-18 17:55

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tasktracker', '0008_auto_20200713_2121'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='task',
            name='template_counter',
        ),
        migrations.RemoveField(
            model_name='task',
            name='template_intervals',
        ),
        migrations.AddField(
            model_name='task',
            name='template_task',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='template', to='tasktracker.Task'),
        ),
        migrations.AlterField(
            model_name='task',
            name='decomposite_task',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='decomposite', to='tasktracker.Task'),
        ),
        migrations.AlterField(
            model_name='task',
            name='task_begin',
            field=models.DateTimeField(default=datetime.datetime(2020, 7, 18, 17, 55, 43, 917483)),
        ),
        migrations.AlterField(
            model_name='task',
            name='task_end',
            field=models.DateTimeField(default=datetime.datetime(2020, 7, 18, 17, 55, 43, 917513)),
        ),
    ]
