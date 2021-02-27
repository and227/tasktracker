<template>
  <b-list-group-item href="#" 
    class="flex-column align-items-start my-1" 
    v-on:click.right ="$emit('show-context-menu', $event, task.id)"
    >
      <div class="d-flex w-100 justify-content-between">
        <h5 class="mb-1">{{ index }}. {{ task.descriprion }}</h5>
        <small class="text-muted">{{ task.id }}</small>
      </div>

      <p class="mb-1">
        {{ taskDateTime(task.task_begin) }} - {{ taskDateTime(task.task_end) }}
      </p>

      <small class="text-muted mr-3">{{ task.priority }}</small>
      <small class="text-muted mr-3">{{ task.task_state }}</small>
      <small class="text-muted mr-3">{{ task.task_type }}</small>
      <small class="text-muted mr-3">{{ task.traking_type }}</small>
  </b-list-group-item>
</template>

<script>
export default {
    props: {
        task: {
            type: Object,
            required: true
        },
        index: Number
    },
    methods: {
        taskDateTime(unix_time) {
            let date = new Date(unix_time * 1000)
            return date.toLocaleDateString("ru-RU", {
                    year: 'numeric',
                    month: 'short',
                    day: '2-digit',
                    weekday: 'short' }) + ' ' +
                date.toLocaleTimeString("ru-RU", {
                    hour12 : true,
                    hour:  "2-digit",
                    minute: "2-digit",
                    second: "2-digit"
                })
        }

    }
}
</script>

<style scoped>
</style>