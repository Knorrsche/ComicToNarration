<script setup>
import { ref } from 'vue';
import SidebarMenu from '../components/SidebarMenu.vue'
import Header from '../components/Header.vue'
import Motivation from '../components/Motivation.vue'
import StorytellingFormats from '../components/StorytellingFormats.vue'
import ComicParts from '../components/ComicParts.vue'
import Challenges from '../components/Challenges.vue'
import InteractiveDetectionPage from './InteractiveDetectionPage.vue'
import InteractiveDlPage from './InteractiveDlPage.vue'
import { nextTick } from 'vue';

const sections = [
  { id: "intro", title: "Intro", component: Header },
  { id: "motivation", title: "Motivation", component: Motivation },
  { id: "formats", title: "Storytelling Formats", component: StorytellingFormats },
  { id: "parts", title: "What Makes a Comic", component: ComicParts },
  { id: "challenges", title: "Processing Challenges", component: Challenges },
  { id: "rb", title: "Comic Processing", component: InteractiveDetectionPage },
  { id: "dl", title: "Deep Learning", component: InteractiveDlPage }
];

const scrollContainer = ref(null);

const scrollToSection = async (id) => {
  try {
    await nextTick();
    const container = scrollContainer.value;
    if (!container) {
      console.warn('scrollToSection: scroll container not found');
      return;
    }

    const target = container.querySelector(`#${id}`);
    if (!target) {
      console.warn(`scrollToSection: No element found with id "${id}"`);
      return;
    }

    container.scrollTo({
      top: target.offsetTop,
      behavior: 'smooth',
    });
  } catch (err) {
    console.error('scrollToSection error:', err);
  }
};
</script>

<template>
  <div class="layout">
    <SidebarMenu :sections="sections" @navigate="scrollToSection" />

    <div class="scroll-container" ref="scrollContainer">
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
.scroll-container {
  flex: 1;
  height: 100vh;
  overflow-y: auto;
  scroll-behavior: smooth;
  scroll-snap-type: y mandatory;
}

.scroll-container::-webkit-scrollbar {
  width: 0;
  height: 0;
}

.scroll-container {
  scrollbar-width: none;
  -ms-overflow-style: none;
}

.content-section {
  scroll-snap-align: start;
  min-height: 100vh;
  background: #fff;
  border-radius: 16px;
  box-shadow: 0 4px 20px rgba(0,0,0,0.06);
  padding: 1rem;
  margin-bottom: 1rem;
}
</style>
