import { createRouter, createWebHistory } from 'vue-router'
import ScrollingStartPage from './pages/ScrollingStartingPage.vue'
import InteractiveMlPage from './pages/InteractiveMlPage.vue'
import InteractiveDlPage from "./pages/InteractiveDlPage.vue";

const routes = [
  { path: '/', component: ScrollingStartPage },
  { path: '/ml', component: InteractiveMlPage },
  { path: '/dl', component: InteractiveDlPage },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

export default router
