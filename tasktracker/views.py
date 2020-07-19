from django.http import HttpResponse
from django.shortcuts import render
from .models import Task, PRIORYITY_TYPES, PERIOD_TYPES, TRAKING_TYPES
import json
from datetime import datetime, timezone
import re

def add_task(json_data):
    if not {'desr', 'priority', 'period', 'is_habit', 'traking', 'datetime_start'}.issubset(set(json_data)):
        print('attribute error')
        return

    new_task = Task()
    for key in json_data:
        val = json_data[key]
        # desr
        if key == 'desr':
            new_task.descriprion = val
        # priority
        elif key == 'priority':
            for sh, lg in PRIORYITY_TYPES:
                if val == lg:
                    new_task.priority = sh
                    break
            else: 
                print('attribute error')
                return
        # period        
        elif key == 'period':
            for sh, lg in PERIOD_TYPES:
                if val == lg:
                    new_task.period = sh
                    break
            else: 
                print('attribute error')
                return
        # traking
        elif key == 'traking':
            for sh, lg in TRAKING_TYPES:
                if val == lg:
                    new_task.traking_type = sh
                    break
            else: 
                print('attribute error')
                return
        # is_habit   
        elif key == 'is_habit':
            new_task.is_habit = True if val == 'True' else False
        elif key == 'datetime_start' and val != '':
            tmp_dt = datetime.strptime(val, "%m/%d/%Y %I:%M %p")
            new_task.task_begin = tmp_dt
        elif key == 'datetime_end' and val != '':
            tmp_dt = datetime.strptime(val, "%m/%d/%Y %I:%M %p")
            new_task.task_end = tmp_dt
        elif key == 'parent_task':
            pass
            # tmp_dt = Task.objects.get(descriprion=val).id
            # new_task.decomposite_task = tmp_dt
        # template
        elif key == 'template_intervals':   
            if not {'active_intervals', 'exclude_selected', 'template_counter'}.issubset(set(val)):
                print('attribute error')
                return

            # active_intervals
            ranges = re.findall(r'[0-9]{1,2}-[0-9]{1,2}', val['active_intervals'])
            active_intervals = val['active_intervals'].split(',')
            for r in ranges:
                active_intervals.remove(r)
            if len(active_intervals) > 0 and active_intervals[0] != '':
                active_intervals = list(map(int, active_intervals))
            ranges = [range(int(r.split('-')[0]), int(r.split('-')[1])+1) for r in ranges]
            for r in ranges:
                active_intervals.extend(r)

            if val['exclude_selected'] == 'True':
                active_intervals = [i for i in range(0,{ 'D' : 7, 'W' : 4, 'M' : 12, 'Y' : 10, 'C' : 0, 'G': 0, 'F' : 0 }[new_task.period]) if i not in active_intervals]

            # add all templates for current task
            if val['template_counter'] != '':
                for interval in range(0, int(val['template_counter'])):
                    dt = new_task.task_begin
                    dt.month = dt.month + interval
                    for point in active_intervals:
                        dt.day = dt.day + point
                        Task.objects.create(period=new_task.period, descriprion=new_task.descriprion, priority=new_task.priority, is_habit=new_task.is_habit, traking_type=new_task.traking_type, task_begin=dt)                   
    
    val = 4
    Task.save(new_task)
    val = 5
    val = 10


def check_time(period_type, start, end):
    res = False
    cur_time = datetime.now()
    start_time = datetime.strptime(start, "%m/%d.%Y %I.%M %p\n")
    end_time = datetime.strptime(end, "%m/%d.%Y %I.%M %p\n")
    if period_type == 'D':
        if cur_time.day >= start_time.day and cur_time.day <= end_time.day:
            res = True
    elif period_type == 'W':
        if cur_time.week >= start_time.week and cur_time.week <= end_time.week:
            res = True
    elif period_type == 'M':
        if cur_time.month >= start_time.month and cur_time.month <= end_time.month:
            res = True
    elif period_type == 'Y':
        if cur_time.year >= start_time.year and cur_time.year <= end_time.year:
            res = True
    else:
        res = True

    return res

def print_date(list_type):
    if type(list_type) == str:
        if list_type[0] == 'd':
            print('day')
            day = list_type[1:3]
            month = list_type[3:5]
            year = list_type[5:7]
            print(day, month, year)
        elif list_type[0] == 'w':
            print('week')
            week = list_type[1]
            month = list_type[2:4]
            year = list_type[4:6]
            print(week, month, year)
        elif list_type[0] == 'm':
            print('month')
            month = list_type[1:3]
            year = list_type[3:5]
            print(month, year)
        elif list_type[0] == 'y':
            print('year')
            year = list_type[1:3]
            print(year)
        elif list_type[0] == 'g':
            print('global')
        elif list_type[0] == 'f':
            print('free')

def default_tasks():
    Task.objects.all().delete()
    tasks = Task.objects.all()
    if len(tasks) == 0:
        Task.objects.create(period='D', descriprion='learn python', priority='M', is_habit=True, traking_type='U')
        Task.objects.create(period='D', descriprion='learn english', priority='M', is_habit=True, traking_type='U')
        Task.objects.create(descriprion='workout', priority='M', is_habit=True, traking_type='U')
        Task.objects.create(descriprion='homework', priority='M', is_habit=True, traking_type='U')
        
        Task.objects.create(period='D', descriprion='task1', priority='M', is_habit=True, traking_type='F', task_begin=datetime.now())
        Task.objects.create(period='D', descriprion='task2', priority='M', is_habit=True, traking_type='F', task_begin=datetime.now())
        Task.objects.create(period='D', descriprion='task3', priority='M', is_habit=True, traking_type='F', task_begin=datetime(2020, 7, 15, 0, 0, 0, 0))
        Task.objects.create(period='D', descriprion='task4', priority='M', is_habit=True, traking_type='F', task_begin=datetime(2020, 7, 16, 0, 0, 0, 0))
        Task.objects.create(period='D', descriprion='task5', priority='M', is_habit=True, traking_type='F', task_begin=datetime(2020, 7, 16, 0, 0, 0, 0))
        Task.objects.create(period='D', descriprion='task6', priority='M', is_habit=True, traking_type='F', task_begin=datetime(2020, 7, 16, 0, 0, 0, 0))
        Task.objects.create(period='D', descriprion='task7', priority='M', is_habit=True, traking_type='F', task_begin=datetime(2020, 7, 16, 0, 0, 0, 0))
        Task.objects.create(period='D', descriprion='task8', priority='M', is_habit=True, traking_type='F', task_begin=datetime(2020, 7, 17, 0, 0, 0, 0))
        Task.objects.create(period='D', descriprion='task9', priority='M', is_habit=True, traking_type='F', task_begin=datetime(2020, 7, 17, 0, 0, 0, 0))
        Task.objects.create(period='M', descriprion='task10', priority='M', is_habit=True, traking_type='F', task_begin=datetime(2020, 8, 16, 0, 0, 0, 0))
        Task.objects.create(period='Y', descriprion='task11', priority='M', is_habit=True, traking_type='F', task_begin=datetime(2021, 8, 16, 0, 0, 0, 0))

        tasks = Task.objects.all()
    print(1, tasks)

def get_tasks(list_type):
    if list_type[0] == 'd':
        day, month, year = list_type[1:3], list_type[3:5], list_type[5:7]
        year = '20' + year
        now = datetime(int(year), int(month), int(day), 0, 0, 0, 0)
        tasks = Task.objects.filter(period='D', task_begin__day=now.day, task_begin__month=now.month, task_begin__year=now.year)
        tasks2 = [repr(task) for task in tasks]
        # add template tasks
        for task in tasks:
            tasks2.extend([repr(task) for task in Task.objects.filter(period='D', template=task.id)])

            
    elif list_type[0] == 'w':
        week, month, year = list_type[1], list_type[2:4], list_type[4:6]
        year = '20' + year
        now = datetime(int(year), int(month), 0, 0, 0, 0, 0) #todo
        tasks = Task.objects.filter(period='W')
        tasks2 = [repr(task) for task in tasks.filter(period='W', task_begin__year=now.year, task_begin__month=now.month)]
        for task in tasks:
            for repetition in range(0,task.template_counter):
                for point in range(0,4):
                    if task.template_intervals & (1 << point):
                        tasks2.append(repr(task))         
    elif list_type[0] == 'm':
        month, year = list_type[1:3], list_type[3:5]
        year = '20' + year
        now = datetime(int(year), int(month), 1, 0, 0, 0, 0) 
        tasks = Task.objects.filter(period='M')
        tasks2 = [repr(task) for task in tasks.filter(task_begin__year=now.year, task_begin__month=now.month)]
        for task in tasks:
            for repetition in range(0,task.template_counter):
                for point in range(0,12):
                    if task.template_intervals & (1 << point):
                        tasks2.append(repr(task))   
    elif list_type[0] == 'y':
        year = list_type[1:3]
        year = '20' + year
        now = datetime(int(year), 0, 1, 0, 0, 0, 0) 
        tasks = Task.objects.filter(period='Y')
        tasks2 = [repr(task) for task in tasks.filter(task_begin__year=now.year)]
        for task in tasks:
            for repetition in range(0,task.template_counter):
                for point in range(0,10):
                    if task.template_intervals & (1 << point):
                        tasks2.append(repr(task))   

    return tasks2

# ------------------------------------------------------------------------------  
def general_task_list(request):
    default_tasks()
    return render(request, 'tasktracker/base_tasklist.html') 

def task_list(request, list_type):   
    if request.is_ajax():
        if request.method == 'POST':
            json_data = json.loads(request.body)
            add_task(json_data)
        print('ajax', request.method)
        tasks = get_tasks(list_type)
        tasks = json.dumps({'tasks': tasks})
        print(3, tasks)
        return HttpResponse(tasks, content_type="application/json")
    else:
        return render(request, 'tasktracker/base_tasklist.html')

def calendar_view(request):
    print('calendar work')
    return render(request, 'tasktracker/calendar.html') 
