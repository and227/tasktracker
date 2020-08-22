# Create your tasks here
from __future__ import absolute_import, unicode_literals

from celery import shared_task
from celery.task import periodic_task
from celery.schedules import crontab
from datetime import timedelta 
from .models import Task

@periodic_task(run_every=(timedelta(seconds=15)), name="update_state")
def update_tasks_num():
    count = len(Task.objects.all())
    print("Current tasks num", count)

@shared_task
def update_db_state():
    print("Current tasks state")

@shared_task
def update_statistic():
    print("Current statistic")

@shared_task
def add(x, y):
    return x + y


@shared_task
def mul(x, y):
    return x * y


@shared_task
def xsum(numbers):
    return sum(numbers)
