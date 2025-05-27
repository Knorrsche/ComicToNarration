<script setup>
import { ref } from 'vue';

import panelImage from '../assets/panel.png';
import gutterImage from '../assets/scene.png';
import bubbleImage from '../assets/speaking_type.png';
import entityImage from '../assets/crowded_entity.png';

const concepts = [
  {
    src: panelImage,
    label: 'Comic Panel',
    explanation:
      'Panels are the fundamental building blocks of comic storytelling. Each panel captures a specific moment in time, and their size, shape, and arrangement help determine pacing, emphasis, and flow. Larger panels can highlight important moments, while smaller ones can accelerate the action.'
  },
  {
    src: gutterImage,
    label: 'Gutter',
    explanation:
      'Gutters are the spaces between comic panels. Although empty, they are powerful narrative tools, allowing readers to infer time, motion, or transitions. The interpretation of what happens in the gutter is known as "closure" — a unique storytelling mechanism in sequential art.'
  },
  {
    src: bubbleImage,
    label: 'Speech Bubble',
    explanation:
      'Speech bubbles convey dialogue and internal thoughts. Their shape and style (e.g., jagged for shouting, cloud-like for thoughts) communicate tone and character. The placement and flow of speech bubbles guide the reader’s eye through the story while delivering emotional and narrative context.'
  },
  {
    src: entityImage,
    label: 'Entities (Characters & Objects)',
    explanation:
      'Entities refer to the characters, objects, or symbols within each panel. They are key to narrative comprehension, visual focus, and emotional engagement. Artists use expressive poses, composition, and contrast to emphasize entities and draw the reader’s attention to them.'
  }
];

const currentIndex = ref(0);

const prevConcept = () => {
  if (currentIndex.value > 0) currentIndex.value--;
};

const nextConcept = () => {
  if (currentIndex.value < concepts.length - 1) currentIndex.value++;
};
</script>

<template>
  <div class="container">
    <h1>Comic Parts</h1>
    <div class="viewer">
      <div class="explanation-box">
        <h3>{{ concepts[currentIndex].label }}</h3>
        <p>{{ concepts[currentIndex].explanation }}</p>
      </div>

      <div class="image-viewer">
        <button class="nav-button" @click="prevConcept" :disabled="currentIndex === 0">◀</button>

        <div class="image-container">
          <img :src="concepts[currentIndex].src" :alt="concepts[currentIndex].label" />
          <div class="caption">{{ concepts[currentIndex].label }}</div>
        </div>

        <button class="nav-button" @click="nextConcept" :disabled="currentIndex === concepts.length - 1">▶</button>
      </div>
    </div>
  </div>
</template>

<style scoped>
.container {
  max-width: 1100px;
  margin: 30px auto;
  font-family: Arial, sans-serif;
  text-align: center;
}

.viewer {
  display: flex;
  align-items: flex-start;
  gap: 30px;
  justify-content: center;
  flex-wrap: wrap;
}

.explanation-box {
  flex: 1 1 300px;
  background-color: #f9f9f9;
  padding: 15px;
  border-radius: 8px;
  box-shadow: 0 0 8px rgba(0, 0, 0, 0.1);
  text-align: left;
  min-height: 400px;
}

.explanation-box h3 {
  margin-bottom: 10px;
  font-size: 1.3rem;
  color: #444;
}

.explanation-box p {
  font-size: 1rem;
  color: #555;
  line-height: 1.4;
}

.image-viewer {
  display: flex;
  align-items: center;
  gap: 10px;
}

.nav-button {
  background-color: #007bff;
  color: white;
  border: none;
  padding: 10px 15px;
  font-size: 1.3rem;
  cursor: pointer;
  border-radius: 5px;
  user-select: none;
}

.nav-button:disabled {
  background-color: #ccc;
  cursor: not-allowed;
}

.image-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  max-width: 400px;
  width: 100%;
}

.image-container img {
  max-width: 60%;
  border-radius: 6px;
  object-fit: contain;
  box-shadow: 0 0 12px rgba(0, 0, 0, 0.2);
  margin-bottom: 8px;
}

.caption {
  font-weight: bold;
  font-size: 1.1rem;
  color: #333;
}
</style>
