from rest_framework import serializers

from .models import Task, Template, PRIORYITY_TYPES, PERIOD_TYPES, TRAKING_TYPES, TASK_TYPES, TIMER_STATES, TASK_STATE

from datetime import datetime

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

# class SelfRelativeField(serializers.ModelSerializer):
#     def to_representation(self, value):
#         serializer = self.parent.parent.__class__(value, context=self.context)
#         return serializer.data

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
    # decomposite_task = SelfRelativeField(many=True)
    # decomposite_task = SelfRelativeField(required=False)
    # template_intervals = TemplateSerializer(source='template_of_set') # serializers.RelatedField

    class Meta:
        model = Task
        fields = '__all__'
        validators = []
        extra_kwargs = {
            'timer_state': {'required': False},
            'decomposite_task': {'required': False},
            'template_of': {'required': False},
            'task_state': {'required': False},
        }

    # def get_validation_exclusions(self):
    #     exclusions = super(TaskSerializer, self).get_validation_exclusions()
    #     return exclusions + ['task_end']

    # def get_fields(self):
    #     fields = super(TaskSerializer, self).get_fields()
    #     subtasks = Task.objects.filter(fields['decomposite_task'])
    #     fields['decomposite_task'] = TaskSerializer(subtasks, many=True)
    #     return fields

    def to_representation(self, obj):
        subtasks = Task.objects.filter(decomposite_task=obj)
        if len(subtasks) > 0:
            # ex = subtasks.values('id')
            # self.instance.exclude(id__in=ex)
            self.fields['subtasks'] = TaskSerializer(subtasks, many=True)      
        return super(TaskSerializer, self).to_representation(obj)

    def create(self, validated_data):
        # add main task
        to_add = Task()
        to_templ = None
        fill_task_params(validated_data, to_add)   
        Task.save(to_add)

         # add template params 
        if ('template_intervals' in validated_data) and validated_data['template_intervals'] != '':   
            if {'active_intervals', 'exclude_selected', 'template_counter'}.issubset(set(validated_data['template_intervals'])):
                to_templ = Template()
                to_templ.template_to = to_add
                active_intervalss = fill_template_params(validated_data['template_intervals'], to_templ)
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

        return to_add

    def update(self, instance, validated_data):
        # edit main task
        fill_task_params(validated_data, instance) 
        instance.save()

        # edit template params 
        try:
            to_templ = Template.objects.get(template_to=instance)
        except Template.DoesNotExist:
            to_templ = None

        if ('template_intervals' in validated_data) and validated_data['template_intervals'] != '':   
            if {'active_intervals', 'exclude_selected', 'template_counter'}.issubset(set(validated_data['template_intervals'])):            
                # 1. no template need to create
                if to_templ == None:
                    to_templ = Template()  
                # 2. is template, change params             
                to_templ.template_to = instance
                active_intervalss = fill_template_params(validated_data['template_intervals'], to_templ)
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
        templates = Task.objects.filter(template_of=instance)
        templates.delete()

        # add template tasks
        if to_templ != None:
            for interval in range(1, to_templ.template_counter + 1):
                dt = instance.task_begin
                dt1 = instance.task_end
                dt = dt.replace(month = dt.month + interval) 
                dt1 = dt1.replace(month = dt1.month + interval) 
                for point in active_intervalss:
                    dt = dt.replace(day = point)  
                    dt1 = dt1.replace(day = point)
                    template = Task()
                    copy_template(template, instance)
                    template.template_of = instance
                    template.task_begin = dt
                    template.task_end = dt1        
                    Task.save(template)   

        return instance