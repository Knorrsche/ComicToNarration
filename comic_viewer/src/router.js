import { createRouter, createWebHistory } from 'vue-router'

import HeaderPage from './pages/HeaderPage.vue'
import InfoBoxPage from './pages/InfoBoxPage.vue'
import GraphicNovelDifferencePage from './pages/GraphicNovelDifferencePage.vue'
import ComicPartsPage from './pages/ComicPartsPage.vue'
import ChallengesPage from './pages/ChallengesPage.vue'

import InteractiveMlPage from './pages/InteractiveMlPage.vue'
import InteractiveDlPage from './pages/InteractiveDlPage.vue'
import ComicViewerPage from './pages/ComicViewerPage.vue'

const routes = [
  { path: '/', component: HeaderPage },
  { path: '/info', component: InfoBoxPage },
  { path: '/gn-diff', component: GraphicNovelDifferencePage },
  { path: '/parts', component: ComicPartsPage },
  { path: '/challenges', component: ChallengesPage },
  { path: '/ml', component: InteractiveMlPage },
  { path: '/dl', component: InteractiveDlPage },
  { path: '/viewer/:comic', name: 'ComicViewer', component: ComicViewerPage, props: true },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

export default router
