# Generated by Django 3.0.7 on 2020-07-09 20:35

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('descriprion', models.CharField(db_index=True, max_length=128)),
                ('priority', models.CharField(choices=[('L', 'Low'), ('M', 'Medium'), ('H', 'High')], default='M', max_length=1)),
                ('is_habit', models.BooleanField(default=False)),
                ('traking_type', models.CharField(choices=[('U', 'Untracking'), ('F', 'Fixed'), ('P', 'Period')], default='U', max_length=1)),
                ('task_begin', models.DateTimeField(default=datetime.datetime(2020, 7, 9, 20, 35, 55, 145400))),
                ('task_end', models.DateTimeField(default=datetime.datetime(2020, 7, 9, 20, 35, 55, 145423))),
                ('lost_time', models.TimeField(default='20:35')),
                ('timer_state', models.CharField(choices=[('I', 'Idle'), ('A', 'Active'), ('P', 'Paused')], default='I', max_length=1)),
                ('period', models.CharField(choices=[('D', 'Day'), ('W', 'Week'), ('M', 'Month'), ('Y', 'Year'), ('C', 'Decade'), ('G', 'Global'), ('F', 'Free')], default='F', max_length=1)),
                ('template_intervals', models.IntegerField(default=0)),
                ('template_counter', models.IntegerField(default=0)),
                ('decomposite_task', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='tasktracker.Task')),
            ],
        ),
    ]
