<template>
<div>
    <!-- Using value -->
    <div class="mx-2 my-2">
        <b-button block variant="primary" v-b-modal="'my-modal'">Add new task</b-button>
    </div>
    <!-- The modal -->
    <b-modal 
        id="my-modal"
        title="Enter task parameters"
        @show="resetModal"
        @hidden="resetModal"
        @ok="handleOk($event)"
    >
        <b-form>
        <b-form-group
            id="input-group-1"
            label="Add your description:"
            label-for="textarea-1"
        >
            <b-form-textarea
            id="textarea-1"
            v-model="selectedTaskGetter.descriprion"
            placeholder="Enter something..."
            rows="3"
            max-rows="6"
            >{{ selectedTaskGetter.descriprion }}</b-form-textarea>
        </b-form-group>

        <b-form-select
            class="mt-3"
            v-model="selectedTaskGetter.priority"
            :options="priorityType"
            >{{ selectedTaskGetter.priority }}</b-form-select
        >
        <b-form-select
            class="mt-3"
            v-model="selectedTaskGetter.traking_type"
            :options="periodType"
            >{{ selectedTaskGetter.traking_type }}</b-form-select
        >

        <div v-if="selectedTaskGetter.traking_type === 'Fixed'" class="mt-3">
            <div>
            <label for="start-datepicker">Start time</label>
            <b-form-datepicker 
                id="start-datepicker"
                :date-format-options="{ year: 'numeric', month: 'short', day: '2-digit', weekday: 'short' }"
                locale="ru"
                v-model="startTaskDate" 
                class="mb-2"
            >
            </b-form-datepicker>
            <b-form-timepicker 
                v-model="startTaskTime"
            >
            </b-form-timepicker>
            </div>
            <div>
            <label for="end-datepicker">End time</label>
            <b-form-datepicker 
                id="end-datepicker"
                :date-format-options="{ year: 'numeric', month: 'short', day: '2-digit', weekday: 'short' }"
                locale="ru"
                v-model="endTaskDate"
                class="mb-2"
            >
            </b-form-datepicker>
            <b-form-timepicker
                v-model="endTaskTime"
            >
            </b-form-timepicker>
            </div>
        </div>

        <div v-if="selectedTaskGetter.traking_type === 'Period'" class="mt-3">
            <label for="end-timeicker">Set task time</label>
            <b-form-timepicker id="end-timeicker" v-model="taskPeriod"></b-form-timepicker>
        </div>
        </b-form>
    </b-modal>
</div>
</template>

<script>
import { mapGetters } from 'vuex' 

export default {
    name: 'AddTask',
    props: {
      task: Object,
      action: String
  },
  data() {
    return {
      priorityType: ["Low", "Medium", "High"],
      periodType: ["Untracked", "Fixed", "Period"],
      startDate: '',
      endDate: '',      
      startTime: '',
      endTime: '',
      taskPeriod: ''
    };
  },
    computed: {
        ...mapGetters(['tasksGetter', 'listTypeGetter',
                'selectedTaskGetter', 'selectedActionGetter']),
        startTaskDate: {
            get: function() {
                return this.$store.getters.selectedTaskDateGetter(1)
            },
            set: function(value) {
                this.$store.commit('setSelectedTaskStartDate', value)
            }
        },
        startTaskTime: {
            get: function() {
                return this.$store.getters.selecterTaskTimeGetter(1)
            },
            set: function(value) {
                this.$store.commit('setSelectedTaskStartTime', value)
            }
        },
        endTaskDate() {
            return this.$store.getters.selectedTaskDateGetter(1)
        },
        endTaskTime() {
            return this.$store.getters.selecterTaskTimeGetter(1)
        },
    }, 
  methods: {
    resetModal() {

    },
    handleOk(event) {
        // Prevent modal from closing
        event.preventDefault()
        // Trigger submit handler
        if (this.action === 'edit-task') {
            console.log('task edited')
        } 
        else {
            this.$store.dispatch('addTask', this.selectedTaskGetter)
            console.log('task added')
        }
    },
    onChange(event) {
      alert(event.target.value);
    },
  },
};
</script>

<style scoped>
</style>