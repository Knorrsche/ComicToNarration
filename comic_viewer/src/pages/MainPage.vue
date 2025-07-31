<script setup>
import { ref } from 'vue'

import HeaderPage from './HeaderPage.vue'
import InfoBoxPage from './InfoBoxPage.vue'
import GraphicNovelDifferencePage from './GraphicNovelDifferencePage.vue'
import ComicPartsPage from './ComicPartsPage.vue'
import ChallengesPage from './ChallengesPage.vue'
import InteractiveMlPage from './InteractiveMlPage.vue'
import InteractiveDlPage from './InteractiveDlPage.vue'

// Sections for menu
const sections = [
  { id: "header", title: "Intro", component: HeaderPage },
  { id: "info", title: "Visual Impariment", component: InfoBoxPage },
  { id: "gn-diff", title: "Graphic Novels", component: GraphicNovelDifferencePage },
  { id: "parts", title: "Parts of Comics", component: ComicPartsPage },
  { id: "challenges", title: "Challenges", component: ChallengesPage },
  { id: "ml", title: "Machine Learning", component: InteractiveMlPage },
  { id: "dl", title: "Deep Learning", component: InteractiveDlPage }
]

const isMenuOpen = ref(false)
const toggleMenu = () => {
  isMenuOpen.value = !isMenuOpen.value
}
</script>

<template>
  <div class="layout">
    <!-- Always visible hamburger -->
    <button class="hamburger" @click="toggleMenu" aria-label="Toggle Menu">☰</button>

    <!-- Sidebar overlay -->
    <nav class="sidebar" :class="{ open: isMenuOpen }">
      <ul>
        <li v-for="section in sections" :key="section.id">
          <a :href="'#' + section.id" @click="isMenuOpen = false">{{ section.title }}</a>
        </li>
      </ul>
    </nav>

    <!-- Scrollable content -->
    <div class="scroll-container">
<section
  v-for="section in sections"
  :key="section.id"
  :id="section.id"
  class="content-section"
>

  <!-- Render the component -->
        <component :is="section.component" :title="section.title" />
</section>
    </div>
  </div>
</template>

<style>
#app{
  padding:0rem;
}
body, html {
  margin: 0;
  padding: 0;
  height: 100%;
}

.layout {
  display: flex;
  height: 100vh;
  overflow: hidden;
}

/* Always visible hamburger */
.hamburger {
  position: fixed;
  top: 1rem;
  left: 1rem;
  z-index: 1100;
  font-size: 1.5rem;
  background: rgba(218, 116, 52, 0.95);
  color: white;
  border: none;
  padding: 0.5rem 0.7rem;
  border-radius: 4px;
  cursor: pointer;
}


.container{
  padding: 0rem;
}

/* Sidebar overlay (hidden by default) */
.sidebar {
  position: fixed;
  top: 0;
  left: -250px;
  height: 100vh;
  width: 250px;
  background-color: #da7434;
  padding-top: 2rem;
  z-index: 1000;
  transition: left 0.3s ease;
}

.sidebar.open {
  left: 0;
}

.sidebar ul {
  list-style: none;
  padding: 0;
  margin: 0;
}

.sidebar li {
  margin: 1.5rem 0;
  text-align: center;
}

.sidebar a {
  color: white;
  text-decoration: none;
  font-weight: bold;
  transition: color 0.3s ease;
  display: block;
  padding: 0.5rem 0;
}

.sidebar a:hover,
.sidebar a.active {
  color: #00bfff;
}

/* Scrollable content */
.scroll-container {
  height: 100vh;
  width: 100vw;
  overflow-y: auto;
  scroll-behavior: smooth;
  padding: 1rem; /* default desktop padding */
}

.scroll-container::-webkit-scrollbar {
  display: none;
}

.content-section {
  margin-bottom: 3rem;
  background: #f8f8f8;
  padding: 0rem;
  border-radius: 8px;
}

/* Remove padding for mobile to use full width */
@media (max-width: 768px) {
  .scroll-container {
    padding-left: 0;
    padding-right: 0;
  }

  .content-section {
    border-radius: 0; /* make it look like full screen cards */
  }
}
</style>
