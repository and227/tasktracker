from django.db import models
import datetime
import time
import json
from django.utils import timezone

PERIOD_TYPES = (('D','Day'), ('W','Week'), ('M','Month'), ('Y','Year'), ('C','Decade'), ('G','Global'), ('F','Free'))
PRIORYITY_TYPES = (('L','Low'), ('M','Medium'), ('H','High'))
TRAKING_TYPES = (('U','Untracked'), ('F','Fixed'), ('P','Period'))
TIMER_STATES = (('I','Idle'), ('A','Active'), ('P','Paused'))
TASK_STATE =  (('I','Idle'), ('A','Active'), ('P','Paused'), ('C','Complited'))

class Task(models.Model):
    descriprion = models.CharField(max_length=128, db_index=True)
    priority = models.CharField(max_length=1, choices=PRIORYITY_TYPES, default='M')
    is_habit = models.BooleanField(default=False)
    traking_type = models.CharField(max_length=1, choices=TRAKING_TYPES, default='U')
    task_begin = models.DateTimeField(default=datetime.datetime.now())
    task_end = models.DateTimeField(default=datetime.datetime.now())
    lost_time = models.IntegerField(default=0)
    timer_state = models.CharField(max_length=1, choices=TIMER_STATES, default='I')
    decomposite_task = models.ForeignKey(to='Task', on_delete=models.SET_NULL, null=True)
    period = models.CharField(max_length=1, choices=PERIOD_TYPES, default='F')
    template_intervals = models.IntegerField(default=0)
    template_counter = models.IntegerField(default=0)
    task_statistic = models.IntegerField(default=0)
    task_state = models.CharField(max_length=1, choices=TIMER_STATES, default='I')


    def __repr__(self):
        ret = {
           'descriprion' :  self.descriprion,
           'priority' : self.get_priority_display(),
           'task_begin' : self.task_begin.strftime("%Y.%m.%d %H:%M:%S")
        }
        if self.traking_type == 'F':
            ret['task_end'] = self.task_end.strftime("%Y.%m.%d %H:%M:%S")
        elif self.traking_type == 'P':
            ret['lost_time'] = str(self.lost_time)
        return json.dumps(ret)

    def __str__(self):
        if self.traking_type == 'F':
            t = str(self.task_begin) + '-' + str(self.task_end)
        elif self.traking_type == 'P':
            t = str(self.lost_time)
        else:
            t = ''

        return self.descriprion + ' ' + self.get_priority_display() + ' ' + self.get_traking_type_display() + ' ' + t




