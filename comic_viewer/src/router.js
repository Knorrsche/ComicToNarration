import { createRouter, createWebHistory } from 'vue-router'

import MainPage from './pages/MainPage.vue'
import ComicViewerPage from './pages/ComicViewerPage.vue'

const routes = [
  { path: '/', component: MainPage },
  { path: '/viewer/:comic', name: 'ComicViewer', component: ComicViewerPage, props: true },
]

const router = createRouter({
  history: createWebHistory('/comic/'),
  routes,
})

export default router
