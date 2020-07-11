from django.http import HttpResponse
from django.shortcuts import render
from .models import Task, PRIORYITY_TYPES, PERIOD_TYPES, TRAKING_TYPES
import json
from datetime import datetime

def check_period(period_type, active_intervals):
    period = Period.objects.get(period_type=period_type, active_intervals=active_intervals)
    if period == None:
        period = Period(period_type=period_type, active_intervals=active_intervals)
        Period.save(period)

    return period.id

def check_template(period, automatic_addition_cur, automatic_addition_viev):
    template = Template.objects.get(period=period, automatic_addition_cur=automatic_addition_cur, automatic_addition_viev=automatic_addition_viev)
    if template == None:
        template = Template(period=period, automatic_addition_cur=automatic_addition_cur, automatic_addition_viev=automatic_addition_viev)
        Template.save(template)
    
    return template.id

def prepare_period(val):
    # period_type
    for sh, lg in PERIOD_TYPES:
        if val[0] == lg:
            val[0] = sh
            break
    else: 
        print('attribute error')
        return
    # active_intervals
    ranges = re.findall(r'[0-9]{1,2}-[0-9]{1,2}', val[1])
    val[1].remove(ranges)
    ranges = [range(r.split('-')[0], r.split('-')[1]) for r in ranges]
    active_intervals = val[1].split(',')
    for r in ranges:
        active_intervals.extend(r)
    int_active_intervals = 0
    for i in range(0,{ 'D' : 0, 'W' : 7, 'M' : 31, 'Y' : 7, 'C' : 0, 'G': 0, 'F' : 0 }[val[0]]):
        if i in active_intervals:
            int_active_intervals |= 1 << i
    #exclude_selected
    if val[2] == 'True':
        int_active_intervals = ~int_active_intervals

    return val[0], int_active_intervals

def add_task(json_data):
    need_update = False
    
    # debug
    for data in json_data:
        print(data, '=', json_data[data]) 

    if not {'desr', 'priority', 'period', 'is_habit', 'traking_type'}.issubset(set(json_data)):
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
            period_type, active_intervals = prepare_period(val)
            new_task.period = check_period(period_type, active_intervals) 
        # is_habit   
        elif key == 'is_habit':
            new_task.is_habit = True if val == 'True' else False
        elif key == 'datetime_start':
            new_task.task_begin = val
        elif key == 'datetime_end':
            new_task.task_end = val
        elif key == 'parent_task':
           new_task.decomposite_task = val
        # template
        elif key == 'template':   
            period_type, active_intervals = prepare_period(val)
            new_task.period = check_period(period_type, active_intervals)  
            new_task.tenplate = check_template(new_task.period, False, False)  
    
    if {'datetime_start', 'datetime_end'}.issubset(set(json_data)):
        need_update = check_time()  
    else:
        need_update = True
    Task.save(new_task)

    return need_update

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
        
        Task.objects.create(period='D', descriprion='task1', priority='M', is_habit=True, traking_type='F')
        Task.objects.create(period='D', descriprion='task2', priority='M', is_habit=True, traking_type='F')
        Task.objects.create(period='D', descriprion='task3', priority='M', is_habit=True, traking_type='F')
        Task.objects.create(period='D', descriprion='task4', priority='M', is_habit=True, traking_type='F')
        
        tasks = Task.objects.all()
    print(1, tasks)

def get_tasks(list_type):
    if list_type[0] == 'd':
        day, month, year = list_type[1:3], list_type[3:5], list_type[5:7]
        now = datetime(int(year), int(month), int(day), 0, 0, 0, 0)
        tasks = Task.objects.filter(period='D')
    elif list_type[0] == 'w':
        week, month, year = list_type[1], list_type[2:4], list_type[4:6]
        now = datetime(int(year), int(month), 0, 0, 0, 0, 0) #todo
        tasks = Task.objects.filter(period='W')
    elif list_type[0] == 'm':
        month, year = list_type[1:3], list_type[3:5]
        now = datetime(int(year), int(month), 0, 0, 0, 0, 0) 
        tasks = Task.objects.filter(period='M')
    elif list_type[0] == 'y':
        year = list_type[1:3]
        now = datetime(int(year), 0, 0, 0, 0, 0, 0) 
        tasks = Task.objects.filter(period='Y')

    tasks = [repr(task) for task in tasks] 
    print(2, tasks)
    return tasks

# ------------------------------------------------------------------------------  
def general_task_list(request):
    print("list_type1")
    return task_list(request, None)       

def task_list(request, list_type):   
    print("list_type")
    print_date(list_type)
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
        default_tasks()
        return render(request, 'tasktracker/base_tasklist.html') 

def calendar_view(request):
    print('calendar work')
    return render(request, 'tasktracker/calendar.html') 
