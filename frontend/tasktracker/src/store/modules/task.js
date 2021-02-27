export default {
    state: {
        tasks: [],
        listType: '',
        selectedTask: null,
        selectedAction: ''
    },
    actions: {
        async requestTasks(ctx) {
            if (ctx.state.listType !== '')
                ctx.state.listType += '/'
            const response = await fetch('http://localhost:8000/tasklist/' + ctx.state.listType)
            const tasks = await response.json()
            console.log(typeof(tasks))
            console.log(typeof(tasks.tasks))
            console.log(tasks.tasks)    
            ctx.commit('setTasks', tasks)
        },
        async addTask(ctx, newTask) {
            console.log('adding new task:', newTask)
            const response = await fetch('http://localhost:8000/tasklist/' + ctx.state.listType, {
                method: 'POST',
                body:  JSON.stringify(newTask)
            })
            const tasks = await response.json()
            console.log(typeof(tasks))
            console.log(typeof(tasks.tasks))
            console.log(tasks.tasks)    
            ctx.commit('setTasks', tasks)
        }
    },
    mutations: {
        setTasks(state, tasks) {
            state.tasks = tasks
        },
        setListType(state, newListType) {
            state.listType = newListType
        },
        selectTask(state, task) {
            state.selectedTask = task
        },
        selectAction(state, action) {
            state.selectedAction = action
        },
        setSelectedTaskStartTime(state, value) {
            state.selectedTask.task_begin = value
        },
        setSelectedTaskStartDate(state, value) {
            state.selectedTask.task_begin = value
        }
    },
    getters: {
        tasksGetter(state) {
            return state.tasks
        },
        listTypeGetter(state) {
            return state.listType
        },
        selectedTaskGetter(state) {
            return state.selectedTask
        },
        selectedActionGetter(state) {
            return state.selectAction
        },
        selectedTaskDateGetter: (state) => (type) => {
            if (type) {
                return state.selectedTask.task_begin
            }
        },
        selecterTaskTimeGetter: (state) => (type) => {
            if (type) {
                return state.selectedTask.task_end
            }
        }
    },
}