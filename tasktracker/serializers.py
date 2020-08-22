from rest_framework import serializers

from .models import Task, Template, PRIORYITY_TYPES, PERIOD_TYPES, TRAKING_TYPES, TASK_TYPES, TIMER_STATES, TASK_STATE

from datetime import datetime

import re

def fill_template_params(json_data, new_template):
    # template_statistic
    new_template.template_statistic = 0
    # active_intervals
    new_template.active_intervals = json_data['active_intervals']
    # exclude_selected
    new_template.exclude_selected = True if json_data['exclude_selected'] == 'True' else False
    # template_counter
    new_template.template_counter = 0
    if json_data['template_counter'] != '':
        new_template.template_counter = int(json_data['template_counter'])   

def copy_template(dst, src):
    dst.descriprion = src.descriprion
    dst.priority = src.priority
    dst.task_type = src.task_type
    dst.traking_type = src.traking_type
    dst.lost_time = src.lost_time
    dst.timer_state = src.timer_state
    dst.period = src.period
    dst.task_state = src.task_state

def get_intervals(str_val, excl):
    ranges = re.findall(r'[0-9]{1,2}-[0-9]{1,2}', str_val)
    list_val = str_val.split(',')
    for r in ranges:
        list_val.remove(r)
    if len(str_val) > 0 and list_val[0] != '':
        list_val = list(map(int, list_val))
    ranges = [range(int(r.split('-')[0]), int(r.split('-')[1])+1) for r in ranges]
    for r in ranges:
        list_val.extend(r)
    if excl == True:
        list_val = [i for i in range(0,{ 'D' : 7, 'W' : 4, 'M' : 12, 'Y' : 10, 'C' : 0, 'G': 0, 'F' : 0 }[new_task.period]) if i not in active_intervals]

    return list_val

def fill_task_params(json_data, new_task):
    for key in json_data:
        val = json_data[key]
        # desr
        if key == 'descriprion':
            new_task.descriprion = val
        # priority
        elif key == 'priority':
            new_task.priority = val
        # period        
        elif key == 'period':
            new_task.period = val
        # traking
        elif key == 'traking_type':
            new_task.traking_type = val
        # task_type   
        elif key == 'task_type':
            new_task.task_type = val
        elif key == 'task_begin':
            if val != '':
                new_task.task_begin = val
        elif key == 'task_end':
            if val != '':
                new_task.task_end = val
        elif key == 'decomposite_task':
            if val != '':
                # parent_task = Task.objects.get(id=val.id)
                new_task.decomposite_task = val
        elif key == 'template':
            # add or edit template params 
            if {'active_intervals', 'exclude_selected', 'template_counter'}.issubset(set(val)):
                # 1. no template need to create
                if new_task.template == None:
                    to_templ = Template()
                else:
                    to_templ = new_task.template
                fill_template_params(val, to_templ)
                Template.save(to_templ)
                new_task.template = to_templ 
            else:
                # 3. is template, need to delete 
                if new_task.template != None:
                    to_templ.delete()

class DateTimeField(serializers.DateTimeField):
    def to_representation(self, value):
        return value.strftime("%m/%d/%Y %I:%M %p")

    def to_internal_value(self, data):
        try:
            dt = datetime.strptime(data, "%m/%d/%Y %I:%M %p")
        except Exception as e:
            dt = ''
        return dt


class PriorityField(serializers.CharField):
    def to_representation(self, value):
        for sh, lg in PRIORYITY_TYPES:
            if value == sh:
                return lg
        return None

    def to_internal_value(self, data):
        for sh, lg in PRIORYITY_TYPES:
            if data == lg:
                return sh
        return None     

class TaskTypeField(serializers.CharField):
    def to_representation(self, value):
        for sh, lg in TASK_TYPES:
            if value == sh:
                return lg
        return None

    def to_internal_value(self, data):
        for sh, lg in TASK_TYPES:
            if data == lg:
                return sh
        return None  


class TrakingField(serializers.CharField):
    def to_representation(self, value):
        for sh, lg in TRAKING_TYPES:
            if value == sh:
                return lg
        return None

    def to_internal_value(self, data):
        for sh, lg in TRAKING_TYPES:
            if data == lg:
                return sh
        return None 


class PeriodField(serializers.CharField):
    def to_representation(self, value):
        for sh, lg in PERIOD_TYPES:
            if value == sh:
                return lg
        return None

    def to_internal_value(self, data):
        for sh, lg in PERIOD_TYPES:
            if data == lg:
                return sh
        return None  


class TaskStateField(serializers.CharField):
    def to_representation(self, value):
        for sh, lg in TIMER_STATES:
            if value == sh:
                return lg
        return None

    def to_internal_value(self, data):
        for sh, lg in TIMER_STATES:
            if data == lg:
                return sh
        return None   


class TimerStateField(serializers.CharField):
    def to_representation(self, value):
        for sh, lg in TASK_STATE:
            if value == sh:
                return lg
        return None

    def to_internal_value(self, data):
        for sh, lg in TASK_STATE:
            if data == lg:
                return sh
        return None  

class TemplateSerializer(serializers.ModelSerializer):  # HyperlinkedModelSerializer
    class Meta:
        model = Template
        fields = '__all__'

class TaskSerializer(serializers.ModelSerializer):
    task_begin = DateTimeField(required=False)
    task_end = DateTimeField(required=False)
    priority = PriorityField(required=False)
    task_type = TaskTypeField(required=False)
    traking_type = TrakingField(required=False)
    period = PeriodField(required=False)
    task_state = TaskStateField(read_only=True, required=False)
    timer_state = TimerStateField(read_only=True, required=False)
    template = TemplateSerializer(required=False)

    class Meta:
        model = Task
        fields = '__all__'
        validators = []
        extra_kwargs = {
            'timer_state': {'required': False},
            'decomposite_task': {'required': False},
            'template_of': {'required': False},
            'task_state': {'required': False},
            'template': {'required': False},
        }

    def to_representation(self, obj):
        subtasks = Task.objects.filter(decomposite_task=obj)
        if len(subtasks) > 0:
            self.fields['subtasks'] = TaskSerializer(subtasks, many=True) 
        # self.fields['template'] = TemplateSerializer(obj.template)   
        return super(TaskSerializer, self).to_representation(obj)

    def create(self, validated_data):
        # add main task
        to_add = Task()
        fill_task_params(validated_data, to_add)   
        Task.save(to_add)

        # add template tasks
        if to_add.template != None:
            for interval in range(1, to_add.template.template_counter + 1):
                dt = to_add.task_begin
                dt1 = to_add.task_end
                dt = dt.replace(month = dt.month + interval) 
                dt1 = dt1.replace(month = dt1.month + interval) 
                for point in get_intervals(to_add.template.active_intervals, to_add.template.exclude_selected):
                    dt = dt.replace(day = point)  
                    dt1 = dt1.replace(day = point)
                    template = Task()
                    copy_template(template, to_add)
                    template.template_of = to_add
                    template.task_begin = dt
                    template.task_end = dt1        
                    Task.save(template)

        return to_add

    def update(self, instance, validated_data):
        # edit main task
        fill_task_params(validated_data, instance) 
        instance.save()

        # delete template tasks
        templates = Task.objects.filter(template_of=instance)
        templates.delete()

        # add template tasks
        if instance.template != None:
            for interval in range(1, instance.template.template_counter + 1):
                dt = instance.task_begin
                dt1 = instance.task_end
                dt = dt.replace(month = dt.month + interval) 
                dt1 = dt1.replace(month = dt1.month + interval) 
                for point in get_intervals(instance.template.active_intervals, instance.template.exclude_selected):
                    dt = dt.replace(day = point)  
                    dt1 = dt1.replace(day = point)
                    template = Task()
                    copy_template(template, instance)
                    template.template_of = instance
                    template.task_begin = dt
                    template.task_end = dt1        
                    Task.save(template)   

        return instance