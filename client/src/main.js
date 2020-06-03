import Vue from 'vue'
import App from './App.vue'
import './registerServiceWorker'
import router from './router'
import store from './store'
import feather from 'vue-icon'
import axios from 'axios'
import VueAxios from 'vue-axios'
import Vue2TouchEvents from 'vue2-touch-events'
import PortalVue from 'portal-vue'

Vue.use(PortalVue)
Vue.use(Vue2TouchEvents)
Vue.use(VueAxios, axios)
Vue.use(feather, 'v-icon')

Vue.config.productionTip = false

new Vue({
  router,
  store,
  render: h => h(App)
}).$mount('#app')
