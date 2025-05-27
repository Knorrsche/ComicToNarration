<script setup>
import { ref } from 'vue';

import entityMatch from '../assets/clustering.png';
import speakerID from '../assets/speaker_iden.png';
import sceneDetect from '../assets/scene.png';

const challenges = [
  {
    src: entityMatch,
    label: 'Entity Matching',
    explanation:
      'Entity matching involves recognizing and following the same character across panels, despite changes in angle, pose, or clothing. This task can be difficult for automated systems and even for readers if visual cues are inconsistent. It’s essential for understanding continuity and who is doing what across the page.'
  },
  {
    src: speakerID,
    label: 'Speaker Identification',
    explanation:
      'Identifying which character is speaking is often based on the direction of speech bubbles, character proximity, or visual cues like eye gaze. This can be ambiguous in crowded scenes or when speech bubbles overlap. Readers rely on context, but it remains a major challenge for machine understanding of comics.'
  },
  {
    src: sceneDetect,
    label: 'Scene Detection',
    explanation:
      'Scene detection refers to determining when the story shifts to a new location or time. This can span multiple panels and isn’t always marked clearly. Artists may use color changes, layout shifts, or environmental clues. Interpreting these transitions is key to following the narrative, especially for digital analysis tools.'
  }
];

const currentIndex = ref(0);

const prevChallenge = () => {
  if (currentIndex.value > 0) currentIndex.value--;
};

const nextChallenge = () => {
  if (currentIndex.value < challenges.length - 1) currentIndex.value++;
};
</script>

<template>
  <div class="container">
    <h1>Challenges</h1>
    <div class="viewer">
      <div class="explanation-box">
        <h3>{{ challenges[currentIndex].label }}</h3>
        <p>{{ challenges[currentIndex].explanation }}</p>
      </div>

      <div class="image-viewer">
        <button class="nav-button" @click="prevChallenge" :disabled="currentIndex === 0">◀</button>

        <div class="image-container">
          <img :src="challenges[currentIndex].src" :alt="challenges[currentIndex].label" />
          <div class="caption">{{ challenges[currentIndex].label }}</div>
        </div>

        <button class="nav-button" @click="nextChallenge" :disabled="currentIndex === challenges.length - 1">▶</button>
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
