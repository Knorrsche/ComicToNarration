<script setup>
import { ref } from 'vue';
import example1 from '../assets/Spiderman.jpg';
import example2 from '../assets/vagabond.jpg';
import example3 from '../assets/Graphic_Novel.png';

const images = [
  {
    src: example1,
    label: 'Western Comic',
    explanation:
      'This image shows a typical panel from a Western comic, such as Spiderman. Western comics often feature vivid colors, dynamic panel layouts, and left-to-right reading flow. Action and emotion are conveyed through expressive poses and speech bubbles. Bold lines and strong contrasts help guide the reader’s eye through fast-paced narratives.'
  },
  {
    src: example2,
    label: 'Japanese Manga',
    explanation:
      'This image depicts a panel from a Japanese manga, like Vagabond. Manga is traditionally black and white, read right-to-left, and emphasizes emotion and atmosphere with fine line work and pacing. Storytelling is often cinematic, using varied panel sizes and quiet moments to create depth and reflection.'
  },
  {
    src: example3,
    label: 'Other Graphic Novels',
    explanation:
      'This image represents newer or alternative formats like Korean webtoons or European graphic novels. Webtoons are typically designed for vertical scrolling on digital devices, while European works often combine artistic storytelling with cultural and historical themes. These formats showcase the growing diversity of visual narratives worldwide.'
  }
];

const currentIndex = ref(0);

const prevImage = () => {
  if (currentIndex.value > 0) currentIndex.value--;
};

const nextImage = () => {
  if (currentIndex.value < images.length - 1) currentIndex.value++;
};
</script>

<template>
  <div class="container">
    <h1>Types of Graphic Novels</h1>
    <div class="viewer">
      <div class="explanation-box">
        <h3>{{ images[currentIndex].label }}</h3>
        <p>{{ images[currentIndex].explanation }}</p>
      </div>

      <div class="image-viewer">
        <button class="nav-button" @click="prevImage" :disabled="currentIndex === 0">◀</button>

        <div class="image-container">
          <img :src="images[currentIndex].src" :alt="images[currentIndex].label" />
          <div class="caption">{{ images[currentIndex].label }}</div>
        </div>

        <button class="nav-button" @click="nextImage" :disabled="currentIndex === images.length - 1">▶</button>
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
