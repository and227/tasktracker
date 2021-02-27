<template>
    <div id="my_tasklist">
        <AddTask/>
        <b-list-group class="mx-2">
            <TaskItem
                v-for="(task, i) of tasksGetter.tasks"  
                :key="i"
                @show-context-menu.prevent="handleClick($event, task)"
                v-bind:task="task"
                v-bind:index="i+1"
            />
        </b-list-group>

        <vue-simple-context-menu
            :elementId="'myFirstMenu'"
            :options="taskOptions"
            :ref="'vueSimpleContextMenu'"
            @option-clicked="optionClicked($event)"
        >
        </vue-simple-context-menu>
    </div>
</template>

<script>
import { mapGetters } from 'vuex' 

import TaskItem from './TaskItem.vue'
import AddTask from './AddTask.vue'

export default {
    data() {
        return {
            listType: 'd310121',
            selectedTask: null,
            selectedAction: null,
            taskOptions: [
                {
                    name: 'Add task',
                    slug: 'add-task'
                },
                {
                    name: 'Add subtask',
                    slug: 'add-subtask'
                },
                {
                    name: 'Edit...',
                    slug: 'edit-task'
                },
                {
                    name: 'Remove',
                    slug: 'remove-task'
                }
            ],
        }
    },
    name: 'TaskList',
    components: {
        TaskItem,
        AddTask,
    },
    computed: mapGetters(['tasksGetter', 'listTypeGetter',
        'selectedTaskGetter', 'selectedActionGetter']),
    methods: {
        getTasks() {
            this.$store.commit('setListType', this.listType)
            this.$store.dispatch('requestTasks')
        },
        handleClick (event, task) {
            this.$refs.vueSimpleContextMenu.showMenu(event, task)
        },
        optionClicked (event) {
            this.$store.commit('selectAction', event.option.slug)
            if (event.option.slug === 'add-task') {
                this.$store.commit('selectTask', {
                    descriprion: '',
                    traking_type: "Untracked",
                    priority: "Medium"
                })
                this.$bvModal.show("my-modal")
            } else if (event.option.slug === 'add-subtask') {
                console.log('add subtask')
                this.$bvModal.show("my-modal")
            } else if (event.option.slug === 'edit-task') {
                let copy_task = { ...event.item }
                this.$store.commit('selectTask', copy_task)
                this.$bvModal.show("my-modal")
            } else if (event.option.slug === 'remove-task') {
                console.log('remove task')
            }
        },
    },
    mounted() {
        this.getTasks()
    }
}
</script>

<style scoped>
</style>