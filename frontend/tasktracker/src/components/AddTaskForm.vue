<template>
  <div>
    <b-form @submit="onSubmit($event)" @reset="onReset($event)">
      <b-form-group
        id="input-group-1"
        label="Add your description:"
        label-for="textarea-1"
      >
        <b-form-textarea
          id="textarea-1"
          v-model="taskDescription"
          placeholder="Enter something..."
          rows="3"
          max-rows="6"
        ></b-form-textarea>
      </b-form-group>

      <b-form-select
        class="mt-3"
        v-model="selectedPriority"
        :options="priorityType"
        >{{ selectedPriority }}</b-form-select
      >
      <b-form-select
        class="mt-3"
        v-model="selectedPeriod"
        :options="periodType"
        >{{ selectedPeriod }}</b-form-select
      >

      <div v-if="selectedPeriod === 'Fixed'" class="mt-3">
        <div>
          <label for="start-datepicker">Start time</label>
          <b-form-datepicker id="start-datepicker" v-model="startDate" class="mb-2"></b-form-datepicker>
          <b-form-timepicker v-model="startTime"></b-form-timepicker>
        </div>
        <div>
          <label for="end-datepicker">End time</label>
          <b-form-datepicker id="end-datepicker" v-model="endDate" class="mb-2"></b-form-datepicker>
          <b-form-timepicker v-model="endTime"></b-form-timepicker>
        </div>
      </div>

      <div v-if="selectedPeriod === 'Period'" class="mt-3">
        <label for="end-timeicker">Set task time</label>
        <b-form-timepicker id="end-timeicker" v-model="taskPeriod"></b-form-timepicker>
      </div>
    </b-form>
  </div>
</template>



<script>
// periodType[selectedPeriod]

export default {
    props: {
      task: Object,
      action: String
  },
  data() {
    return {
      taskDescription: "",
      selectedPriority: null,
      priorityType: ["Low", "Medium", "High"],
      selectedPeriod: null,
      periodType: ["Untracked", "Fixed", "Period"],
      startDate: '',
      endDate: '',      
      startTime: '',
      endTime: '',
      taskPeriod: ''
    };
  },
  methods: {
    onSubmit(event) {
      console.log('action permited')
      event.preventDefault();
      alert(JSON.stringify(this.form));
    },
    onReset(event) {
      event.preventDefault();
      // Reset our form values
      this.form.email = "";
      this.form.name = "";
      this.form.food = null;
      this.form.checked = [];
      // Trick to reset/clear native browser form validation state
      this.show = false;
      this.$nextTick(() => {
        this.show = true;
      });
    },
    onChange(event) {
      alert(event.target.value);
    },
    fillTaskProps(task) {
        this.taskDescription = task.descriprion
        this.selectedPriority = task.priority
        this.selectedPeriod = task.traking_type
        this.startDate = task.task_begin
        this.endDate = task.task_end      
    },
  },
  mounted() {
    if (this.action === 'edit-task') {
      this.fillTaskProps(this.task)
    }
  }
};
</script>