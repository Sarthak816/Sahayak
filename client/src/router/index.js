import { createRouter, createWebHistory } from 'vue-router'
import Home from '@/pages/home/Home.vue'
import Services from '@/pages/services/Services.vue'
import Chatbot from '@/pages/chatbot/Chatbot.vue'
import EmployeeLogin from '@/pages/employee/login/Login.vue'
import CreateTicket from '@/pages/employee/tickets/CreateTicket.vue'
import ViewTickets from '@/pages/employee/tickets/ViewTickets.vue'
import { authClient } from '@/lib/auth-client'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home,
  },
  {
    path: '/services',
    name: 'Services',
    component: Services,
  },
  {
    path: '/chatbot',
    name: 'Chatbot',
    component: Chatbot,
  },
  {
    path: '/employee/login',
    name: 'Employee Login',
    component: EmployeeLogin,
  },
  {
    path: '/employee/dashboard',
    name: 'Employee Dashboard',
    component: () => import('@/pages/employee/dashboard/Dashboard.vue'),
    meta: { requiresAuth: true },
  },
  {
    path: '/employee/tickets/create',
    name: 'Create Ticket',
    component: CreateTicket,
  },
  {
    path: '/employee/tickets',
    name: 'View Tickets',
    component: ViewTickets,
  },
]

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes,
})
router.beforeEach(async (to, from, next) => {
  if (to.meta.requiresAuth) {
    const session = await authClient.getSession()
    if (!session) {
      next('/employee/login')
    } else {
      next()
    }
  } else {
    next()
  }
})

export default router
