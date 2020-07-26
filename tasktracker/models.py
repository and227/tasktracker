from django.db import models
import datetime
import time
import json
from django.utils import timezone

PERIOD_TYPES = (('D','Day'), ('W','Week'), ('M','Month'), ('Y','Year'), ('C','Decade'), ('G','Global'), ('F','Free'))
PRIORYITY_TYPES = (('L','Low'), ('M','Medium'), ('H','High'))
TRAKING_TYPES = (('U','Untracked'), ('F','Fixed'), ('P','Period'))
TIMER_STATES = (('I','Idle'), ('A','Active'), ('P','Paused'))
TASK_STATE =  (('I','Idle'), ('P','Failed'), ('C','Complited'))
TASK_TYPES = (('S','Simple'), ('T','Template'), ('D','Decomposite'))

class Task(models.Model):
    descriprion = models.CharField(max_length=128, db_index=True)
    priority = models.CharField(max_length=1, choices=PRIORYITY_TYPES, default='M')
    task_type = models.CharField(max_length=1, choices=TASK_TYPES, default='S')
    traking_type = models.CharField(max_length=1, choices=TRAKING_TYPES, default='U')
    task_begin = models.DateTimeField(default=datetime.datetime.now())
    task_end = models.DateTimeField(default=datetime.datetime.now())
    lost_time = models.IntegerField(default=0)
    timer_state = models.CharField(max_length=1, choices=TIMER_STATES, default='I')
    decomposite_task = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, related_name='decomposite')
    period = models.CharField(max_length=1, choices=PERIOD_TYPES, default='F')
    template_of = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, related_name='templ_of')
    task_state = models.CharField(max_length=1, choices=TIMER_STATES, default='I')

    def __repr__(self):
        ret = {
            'desr' :                        self.descriprion,
            'priority' :                    self.get_priority_display(),
            'datetime_start' :              self.task_begin.strftime("%m/%d/%Y %I:%M %p"),          
            'traking'  :                    self.get_traking_type_display(),
            'period'   :                    self.get_period_display(),
            'task_type' :                   self.get_task_type_display(),
            'datetime_end' :                self.task_end.strftime("%m/%d/%Y %I:%M %p"),
            'lost_time' :                   str(self.lost_time),
            'parent_task' :                 self.decomposite_task.id if self.decomposite_task != None else None,
            'template_intervals' :          ''
        }
        if self.traking_type == 'F':
            ret['datetime_end'] = self.task_end.strftime("%m/%d/%Y %I:%M %p")
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

class Template(models.Model):
    template_to = models.ForeignKey(to='Task', on_delete=models.SET_NULL, null=True, related_name='templ_to')
    active_intervals = models.CharField(max_length=32, db_index=True, default='')
    exclude_selected = models.BooleanField(default=False)
    template_counter = models.IntegerField(default=0)
    template_statistic = models.IntegerField(default=0)

class Statistic(models.Model):
    date_point =  models.DateField(default=datetime.datetime.now())
    task_in_point = models.IntegerField(default=0)
    task_complited = models.IntegerField(default=0)



