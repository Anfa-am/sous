import Vue from 'vue'
import VueRouter from 'vue-router'

Vue.use(VueRouter)

const routes = [
  {
    path: '/explore',
    name: 'Explore',
    component: () => import(/* webpackChunkName: "about" */ '../views/Explore.vue')
  }, {
    path: '/cookbook',
    name: 'Cookbok',
    component: () => import(/* webpackChunkName: "about" */ '../views/Cookbook.vue')
  }, {
    path: '/shopping',
    name: 'Shopping',
    component: () => import(/* webpackChunkName: "about" */ '../views/Shopping.vue')
  }, {
    path: '/prefrences',
    name: 'Prefrences',
    component: () => import(/* webpackChunkName: "about" */ '../views/Prefrences.vue')
  }, {
    path: '*',
    name: 'Welcome',
    component: () => import(/* webpackChunkName: "about" */ '../views/Welcome.vue')
  },

]

const router = new VueRouter({ routes })

export default router
