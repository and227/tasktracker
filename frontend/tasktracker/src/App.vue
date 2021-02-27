<template>
  <div id="app">
    <Header/>
    <Filters/>
    <TaskList
      v-bind:tasks="tasks"
    />
    <Footer/>
  </div>
</template>

<script>
// import HelloWorld from './components/HelloWorld.vue'
import Header from './components/Header.vue'
import Filters from './components/Filters.vue'
import TaskList from './components/TaskList.vue'
import Footer from './components/Footer.vue'

export default {
  name: 'App',
  data() {
    return {
      tasks: [
        "task1",
        "task2",
        "task3",
        "task4",
        "task5",
        "task6",
        "task7",
        "task8",
        "task9",
        "task10",
      ]
    }
  },
  components: {
    Header,
    Filters,
    TaskList,
    Footer,
  }
}
</script>

<style>
/* #app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
} */
</style>
