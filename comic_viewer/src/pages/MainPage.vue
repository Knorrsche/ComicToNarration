<script setup>
import { ref } from 'vue'

import Header from '../components/Header.vue'
import InfoBox from '../components/InfoBox.vue'
import GraphicNovelDifference from '../components/GraphicNovelDifference.vue'
import ComicParts from '../components/ComicParts.vue'
import Challenges from '../components/Challenges.vue'
import InteractiveMlPage from './InteractiveMlPage.vue'
import InteractiveDlPage from './InteractiveDlPage.vue'

const sections = [
  { id: "header", title: "Intro", component: Header },
  { id: "info", title: "Visual Impairment", component: InfoBox },
  { id: "gn-diff", title: "Graphic Novels", component: GraphicNovelDifference },
  { id: "parts", title: "Parts of Comics", component: ComicParts },
  { id: "challenges", title: "Challenges", component: Challenges },
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
    <button
      class="hamburger"
      :class="{ open: isMenuOpen }"
      @click="toggleMenu"
      aria-label="Toggle Menu"
    >
      <span></span>
      <span></span>
      <span></span>
    </button>

    <!-- Sidebar -->
    <nav class="sidebar" :class="{ open: isMenuOpen }">
      <ul>
        <li v-for="section in sections" :key="section.id">
          <a :href="'#' + section.id" @click="isMenuOpen = false">
            {{ section.title }}
          </a>
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
        <component :is="section.component" :title="section.title" />
      </section>
    </div>
  </div>
</template>

<style>
:root {
  --orange-primary: #da7434;
  --orange-light: #ffe9dc;
}

#app {
  font-family: "Inter", "Segoe UI", Tahoma, sans-serif;
}

body, html {
  margin: 0;
  padding: 0;
  height: 100%;
  background: #fafafa;
}

.layout {
  display: flex;
  height: 100vh;
}

/* Modern Hamburger with visible button */
.hamburger {
  position: fixed;
  top: 1rem;
  left: 1rem;
  z-index: 9999;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  width: 40px;
  height: 40px;
  background: white;
  border: 2px solid var(--orange-primary);
  border-radius: 8px;
  padding: 8px;
  cursor: pointer;
  transition: all 0.2s ease;
}

.hamburger:hover {
  background: var(--orange-light);
  transform: scale(1.05);
}

.hamburger span {
  display: block;
  height: 3px;
  background: var(--orange-primary);
  border-radius: 2px;
  transition: 0.3s ease;
}

/* Animation into X */
.hamburger.open span:nth-child(1) {
  transform: translateY(8px) rotate(45deg);
}
.hamburger.open span:nth-child(2) {
  opacity: 0;
}
.hamburger.open span:nth-child(3) {
  transform: translateY(-8px) rotate(-45deg);
}

/* Sidebar */
.sidebar {
  position: fixed;
  top: 0;
  left: -260px;
  height: 100vh;
  width: 250px;
  background: var(--orange-primary);
  box-shadow: 2px 0 8px rgba(0,0,0,0.15);
  padding-top: 4rem;
  z-index: 1500;
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
  margin: 1.2rem 0;
  text-align: center;
}

.sidebar a {
  color: #fff;
  text-decoration: none;
  font-weight: 500;
  font-size: 1rem;
  transition: all 0.3s ease;
}

.sidebar a:hover,
.sidebar a.active {
  color: #ffe9dc;
  text-shadow: 0 0 6px rgba(255, 255, 255, 0.4);
}

/* Scroll container */
.scroll-container {
  flex: 1;
  height: 100vh;
  overflow-y: auto;
  scroll-behavior: smooth;
  scroll-snap-type: y mandatory;
  padding: 1rem;
}

.scroll-container::-webkit-scrollbar {
  display: none;
}

/* Neutral content sections */
.content-section {
  scroll-snap-align: start;
  min-height: 100vh;
  background: #fff;
  border-radius: 16px;
  box-shadow: 0 4px 20px rgba(0,0,0,0.06);
  padding: 1rem;
  margin-bottom: 1rem;
  /* Removed orange border-top */
}

.content-section h1,
.content-section h2,
.content-section h3 {
  color: inherit; /* No forced orange */
}

@media (max-width: 768px) {
  .scroll-container {
    padding: 0;
  }
  .content-section {
    border-radius: 0;
    margin-bottom: 0;
  }
}
</style>
