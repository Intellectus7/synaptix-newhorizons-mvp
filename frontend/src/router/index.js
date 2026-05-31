import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import Documentation from '@/views/Documentation.vue'
import Register from '@/views/Register.vue'
import LoginView from '@/views/LoginView.vue'
import ExploreView from '@/views/ExploreView.vue'
import CreateBotView from '@/views/CreateBotView.vue'

let routes = []

function addRoute(name, component) {
  return {
    path: `/${name}`,
    name: name,
    component: component
  }
}
const oldRoutes = [
    {
      path: '/',
      name: 'home',
      component: HomeView,
    },
    {
      path: '/about',
      name: 'about',
      // route level code-splitting
      // this generates a separate chunk (About.[hash].js) for this route
      // which is lazy-loaded when the route is visited.
      component: () => import('../views/AboutView.vue'),
    }, 
    {
      path: '/chat/:userId',
      name: 'chatUser',
      component: () => import('../views/ChatView.vue'),
    },
]
const docs = addRoute('docs', Documentation)
const register = addRoute('register', Register)
const login = addRoute('login', LoginView)
const explore = addRoute('explore', ExploreView)
const bots = addRoute('bot', CreateBotView)
const newRoutes = [docs, register, login, explore, bots]


function joinRoutes() {
  for (let i of oldRoutes) {
    routes.push(i);
  } 
  for (let j of newRoutes) {
    routes.push(j)
  }
  return routes
}

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: joinRoutes(),
})

export default router
