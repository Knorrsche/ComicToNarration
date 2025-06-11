<script setup>
import { ref, onMounted, onUnmounted } from 'vue'

import Header from '../components/Header.vue'
import InfoBox from "../components/InfoBox.vue";
import GraphicNovelDifference from "../components/GraphicNovelDifference.vue";
import ComicParts from "../components/ComicParts.vue";
import Challenges from "../components/Challenges.vue";

const currentSection = ref('header')

onMounted(() => {
  const sections = document.querySelectorAll('.scroll-container section')
  const observer = new IntersectionObserver(
    (entries) => {
      for (const entry of entries) {
        if (entry.isIntersecting) {
          currentSection.value = entry.target.id
          break
        }
      }
    },
    {
      root: document.querySelector('.scroll-container'),
      threshold: 0.5,
    }
  )

  sections.forEach((section) => observer.observe(section))

  onUnmounted(() => {
    observer.disconnect()
  })
})
</script>

<template>
  <div class="layout">
    <div class="scroll-container">
      <section id="header"><Header /></section>
      <section id="info"><InfoBox /></section>
      <section id="gn-diff"><GraphicNovelDifference /></section>
      <section id="parts"><ComicParts /></section>
      <section id="challenges"><Challenges /></section>
    </div>
  </div>
</template>

<style scoped>
html, body {
  margin: 0;
  padding: 0;
  height: 100%;
  overflow: hidden;
  overscroll-behavior: none;
  -webkit-overflow-scrolling: touch;
}

.layout {
  display: flex;
  height: 100vh;
}

.scroll-container {
  margin-left: 200px;
  height: 100vh;
  width: calc(100vw - 200px);
  overflow-y: scroll;
  scroll-snap-type: y mandatory;
  scroll-behavior: smooth;
  scrollbar-width: none;
  -ms-overflow-style: none;
}

.scroll-container::-webkit-scrollbar {
  display: none;
}

.scroll-container section {
  scroll-snap-align: start;
  height: 100vh;
  padding: 20px;
  box-sizing: border-box;
}
</style>
