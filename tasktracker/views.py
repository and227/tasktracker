from django.http import HttpResponse
from django.shortcuts import render
from .models import Task, Template, Statistic, PRIORYITY_TYPES, PERIOD_TYPES, TRAKING_TYPES, TASK_TYPES
import json
from datetime import datetime, timezone
import re

def fill_task_params(json_data, new_task):
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
        # task_type   
        elif key == 'task_type':
            for sh, lg in TASK_TYPES:
                if val == lg:
                    new_task.task_type = sh
                    break
            else: 
                print('attribute error')
                return           
        elif key == 'datetime_start' and val != '':
            tmp_dt = datetime.strptime(val, "%m/%d/%Y %I:%M %p")
            new_task.task_begin = tmp_dt
        elif key == 'datetime_end' and val != '':
            tmp_dt = datetime.strptime(val, "%m/%d/%Y %I:%M %p")
            new_task.task_end = tmp_dt
        elif key == 'parent_task':
            if val != '':
                parent_task = Task.objects.get(descriprion=val)
                new_task.decomposite_task = parent_task
            else:
                new_task.decomposite_task = None
            # tmp_dt = Task.objects.get(descriprion=val).id
            # new_task.decomposite_task = tmp_dt

def fill_template_params(json_data, new_template):
    # template_statistic
    new_template.template_statistic = 0
    # active_intervals
    new_template.active_intervals = json_data['active_intervals']
    ranges = re.findall(r'[0-9]{1,2}-[0-9]{1,2}', new_template.active_intervals)
    active_intervals = new_template.active_intervals.split(',')
    for r in ranges:
        active_intervals.remove(r)
    if len(active_intervals) > 0 and active_intervals[0] != '':
        active_intervals = list(map(int, active_intervals))
    ranges = [range(int(r.split('-')[0]), int(r.split('-')[1])+1) for r in ranges]
    for r in ranges:
        active_intervals.extend(r)
    # exclude_selected
    new_template.exclude_selected = True if json_data['exclude_selected'] == 'True' else False
    if new_template.exclude_selected == True:
        active_intervals = [i for i in range(0,{ 'D' : 7, 'W' : 4, 'M' : 12, 'Y' : 10, 'C' : 0, 'G': 0, 'F' : 0 }[new_task.period]) if i not in active_intervals]
    # template_counter
    new_template.template_counter = 0
    if json_data['template_counter'] != '':
        new_template.template_counter = int(json_data['template_counter'])   

    return active_intervals

def copy_template(dst, src, ):
    dst.descriprion = src.descriprion
    dst.priority = src.priority
    dst.task_type = src.task_type
    dst.traking_type = src.traking_type
    dst.lost_time = src.lost_time
    dst.timer_state = src.timer_state
    dst.period = src.period
    dst.task_state = src.task_state

def add_task(json_data):
    if not {'desr', 'priority', 'period', 'task_type', 'traking', 'datetime_start'}.issubset(set(json_data)):
        print('attribute error')
        return

    # add main task
    to_add = Task()
    to_templ = None
    fill_task_params(json_data, to_add)   
    Task.save(to_add)

    # add template params 
    if json_data['template_intervals'] != None and json_data['template_intervals'] != '':   
        if {'active_intervals', 'exclude_selected', 'template_counter'}.issubset(set(json_data['template_intervals'])):
            to_templ = Template()
            to_templ.template_to = to_add
            active_intervalss = fill_template_params(json_data['template_intervals'], to_templ)
            Template.save(to_templ)
        else:
            print('attribute error')
            return               

    # add template tasks
    if to_templ != None:
        for interval in range(1, to_templ.template_counter + 1):
            dt = to_add.task_begin
            dt1 = to_add.task_end
            dt = dt.replace(month = dt.month + interval) 
            dt1 = dt1.replace(month = dt1.month + interval) 
            for point in active_intervalss:
                dt = dt.replace(day = point)  
                dt1 = dt1.replace(day = point)
                template = Task()
                copy_template(template, to_add)
                template.template_of = to_add
                template.task_begin = dt
                template.task_end = dt1        
                Task.save(template)

def delete_task(json_data):
    if not {'desr', 'datetime_start'}.issubset(set(json_data)):
        print('attribute error')
        return

    # delete main and template tasks
    tmp_dt = datetime.strptime(json_data["datetime_start"], "%m/%d/%Y %I:%M %p")
    to_del = Task.objects.filter(descriprion=json_data["desr"], task_begin=tmp_dt)
    if len(to_del):
        templates = Task.objects.filter(template_of=to_del[0])
        templates.delete()
        to_del.delete()



def edit_task(old_data, new_data):
    if not {'desr', 'datetime_start'}.issubset(set(old_data)):
        print('attribute error')
        return

    if not {'desr', 'priority', 'period', 'task_type', 'traking', 'datetime_start'}.issubset(set(new_data)):
        print('attribute error')
        return

    to_templ = None

    # edit main task
    tmp_dt = datetime.strptime(old_data["datetime_start"], "%m/%d/%Y %I:%M %p")
    to_edit = Task.objects.get(descriprion=old_data["desr"], task_begin=tmp_dt)
    fill_task_params(new_data, to_edit) 
    to_edit.save()

    # TODO 

    # edit template params 
    try:
        to_templ = Template.objects.get(template_to=to_edit)
    except Template.DoesNotExist:
        to_templ = None

    if new_data['template_intervals'] != None and new_data['template_intervals'] != '':   
        if {'active_intervals', 'exclude_selected', 'template_counter'}.issubset(set(new_data['template_intervals'])):            
            # 1. no template need to create
            if to_templ == None:
                to_templ = Template()  
            # 2. is template, change params             
            to_templ.template_to = to_edit
            active_intervalss = fill_template_params(new_data['template_intervals'], to_templ)
            Template.save(to_templ)
        else:
            print('attribute error')
            return  
    else:
        # 3. is template, need to delete 
        if to_templ != None:
            to_templ.delete()
            to_templ = None

    # delete template tasks
    templates = Task.objects.filter(template_of=to_edit)
    templates.delete()

    # add template tasks
    if to_templ != None:
        for interval in range(1, to_templ.template_counter + 1):
            dt = to_edit.task_begin
            dt1 = to_edit.task_end
            dt = dt.replace(month = dt.month + interval) 
            dt1 = dt1.replace(month = dt1.month + interval) 
            for point in active_intervalss:
                dt = dt.replace(day = point)  
                dt1 = dt1.replace(day = point)
                template = Task()
                copy_template(template, to_edit)
                template.template_of = to_edit
                template.task_begin = dt
                template.task_end = dt1        
                Task.save(template)   


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

    # tasks = Task.objects.all()
    # if len(tasks) == 0:
    #     Task.objects.create(period='D', descriprion='learn python', priority='M', task_type='S', traking_type='U')
    #     Task.objects.create(period='D', descriprion='learn english', priority='M',  task_type='S', traking_type='U')
    #     Task.objects.create(descriprion='workout', priority='M',  task_type='S', traking_type='U')
    #     Task.objects.create(descriprion='homework', priority='M',  task_type='S', traking_type='U')
        
    #     Task.objects.create(period='D', descriprion='task1', priority='M', task_type='S', traking_type='F', task_begin=datetime.now())
    #     Task.objects.create(period='D', descriprion='task2', priority='M', task_type='S', traking_type='F', task_begin=datetime.now())
    #     Task.objects.create(period='D', descriprion='task3', priority='M', task_type='S', traking_type='F', task_begin=datetime(2020, 7, 15, 0, 0, 0, 0))
    #     Task.objects.create(period='D', descriprion='task4', priority='M', task_type='S', traking_type='F', task_begin=datetime(2020, 7, 16, 0, 0, 0, 0))
    #     Task.objects.create(period='D', descriprion='task5', priority='M', task_type='S', traking_type='F', task_begin=datetime(2020, 7, 16, 0, 0, 0, 0))
    #     Task.objects.create(period='D', descriprion='task6', priority='M', task_type='S', traking_type='F', task_begin=datetime(2020, 7, 16, 0, 0, 0, 0))
    #     Task.objects.create(period='D', descriprion='task7', priority='M', task_type='S', traking_type='F', task_begin=datetime(2020, 7, 16, 0, 0, 0, 0))
    #     Task.objects.create(period='D', descriprion='task8', priority='M', task_type='S', traking_type='F', task_begin=datetime(2020, 7, 17, 0, 0, 0, 0))
    #     Task.objects.create(period='D', descriprion='task9', priority='M', task_type='S', traking_type='F', task_begin=datetime(2020, 7, 17, 0, 0, 0, 0))
    #     Task.objects.create(period='M', descriprion='task10', priority='M', task_type='S', traking_type='F', task_begin=datetime(2020, 8, 16, 0, 0, 0, 0))
    #     Task.objects.create(period='Y', descriprion='task11', priority='M', task_type='S', traking_type='F', task_begin=datetime(2021, 8, 16, 0, 0, 0, 0))

    #     tasks = Task.objects.all()
    # print(1, tasks)

def check_task(list_type, json_data):
    if list_type[0] == 'd':
        day, month, year = list_type[1:3], list_type[3:5], list_type[5:7]
        year = '20' + year
        now = datetime(int(year), int(month), int(day), 0, 0, 0, 0) 
        tasks = Task.objects.filter(descriprion=json_data['desr'], period='D', task_begin__day=now.day, task_begin__month=now.month, task_begin__year=now.year)  
        if len(tasks) > 0:
            return True
        else:
            return False

def task_to_dict(task, exclude, level):
    if level > 2:
        return

    template = ''
    is_tmpl = None
    try:
        is_tmpl = Template.objects.get(template_to=task)
    except Exception as e:
        print(e)
    if is_tmpl != None:
        template = {   
            'active_intervals' :            str(is_tmpl.active_intervals),
            'exclude_selected' :            str(is_tmpl.exclude_selected),
            'template_counter' :            str(is_tmpl.template_counter)
        }

    ret = {
        'desr' :                        task.descriprion,
        'priority' :                    task.get_priority_display(),
        'datetime_start' :              task.task_begin.strftime("%m/%d/%Y %I:%M %p"),          
        'traking'  :                    task.get_traking_type_display(),
        'period'   :                    task.get_period_display(),
        'task_type' :                   task.get_task_type_display(),
        'datetime_end' :                task.task_end.strftime("%m/%d/%Y %I:%M %p"),
        'lost_time' :                   str(task.lost_time),
        'template_intervals' :          template
    }
    if task.traking_type == 'F':
        ret['datetime_end'] = task.task_end.strftime("%m/%d/%Y %I:%M %p")
    elif task.traking_type == 'P':
        ret['lost_time'] = str(task.lost_time)

    subtasks = Task.objects.filter(decomposite_task=task)
    if len(subtasks) > 0:
        ret['parent_task'] = []
        for subtask in subtasks:
            st = task_to_dict(subtask, exclude, level+1)
            ret['parent_task'].append(st)
            exclude.append(st)        

    return ret

def get_tasks(list_type):
    if list_type[0] == 'd':
        day, month, year = list_type[1:3], list_type[3:5], list_type[5:7]
        year = '20' + year
        now = datetime(int(year), int(month), int(day), 0, 0, 0, 0)
        tasks = Task.objects.filter(period='D', task_begin__day=now.day, task_begin__month=now.month, task_begin__year=now.year)
        tasks2 = []
        exclude_list = []
        # add simple and decomposite tasks
        for task in tasks:
            task_dict = task_to_dict(task, exclude_list, 0)
            tasks2.append(task_dict)

        tasks2 = [json.dumps(task_dict) for task_dict in tasks2 if task_dict not in exclude_list]
        # add template tasks
        # for task in tasks:
        #     try:
        #         templates = Task.objects.filter(period='D', template_of=task)
        #         for template in templates:
        #             tasks2.append(json.dumps(task_to_dict(template, exclude_list, 0)))
        #     except Exception as e:
        #         print(e)

            
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
    elif list_type[0] == 'f':
        tasks = Task.objects.all()
        tasks2 = []
        exclude_list = []
        # add simple and decomposite tasks
        for task in tasks:
            task_dict = task_to_dict(task, exclude_list, 0)
            tasks2.append(task_dict)

        tasks2 = [json.dumps(task_dict) for task_dict in tasks2 if task_dict not in exclude_list]

    return tasks2

# ------------------------------------------------------------------------------  
def general_task_list(request):
    default_tasks()
    return render(request, 'tasktracker/base_tasklist.html') 

def task_list(request, list_type):   
    if request.is_ajax():
        if request.method == 'POST':
            json_data = json.loads(request.body)
            if json_data["type"] == "add":
                if not check_task(list_type, json_data["data"]):
                    add_task(json_data["data"])
            elif json_data["type"] == "delete":
                delete_task(json_data["data"])
            elif json_data["type"] == "edit":
                edit_task(json_data["old_data"], json_data["data"])
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
