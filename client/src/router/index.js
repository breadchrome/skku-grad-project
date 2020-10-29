import { createRouter, createWebHistory } from '@ionic/vue-router';
import Tabs from '../views/Tabs.vue'

const routes = [
  {
    path: '/',
    component: Tabs,
    children: [
      {
        path: '',
        redirect: 'sleep-analysis'
      },
      {
        path: 'sleep-analysis',
        component: () => import('@/views/SleepAnalysis.vue')
      },
      {
        path: 'settings',
        component: () => import('@/views/Settings.vue')
      }
    ]
  }
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

export default router
