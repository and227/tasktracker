import Vue from 'vue'
import App from './App.vue'
import { BButtonGroup, BListGroup, BootstrapVue, IconsPlugin } from 'bootstrap-vue'

import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap-vue/dist/bootstrap-vue.css'

// import VueSimpleContextMenu from 'vue-simple-context-menu'

import store from './store/index'

import VueSimpleContextMenu from 'vue-simple-context-menu'
Vue.component('vue-simple-context-menu', VueSimpleContextMenu)

Vue.config.productionTip = false

// Make BootstrapVue available throughout your project
Vue.use(BootstrapVue)
// Optionally install the BootstrapVue icon components plugin
Vue.use(IconsPlugin)


// Vue.component('vue-simple-context-menu', VueSimpleContextMenu)
Vue.component('b-button-group', BButtonGroup)
Vue.component('b-list-group', BListGroup)

new Vue({
  store,
  render: h => h(App),
}).$mount('#app')
