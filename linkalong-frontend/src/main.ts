import Vue from 'vue'
import App from './App.vue'
import { routes } from '@/routing'
import VueRouter from 'vue-router'

Vue.use(VueRouter)
Vue.config.productionTip = false

new Vue({
  router: new VueRouter({ routes }),
  render: h => h(App)
}).$mount('#app')
