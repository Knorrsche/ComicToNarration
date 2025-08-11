<script setup>
import { ref, onMounted } from 'vue';

const props = defineProps({
  title: String,
  images: { type: Array, required: true },
  explanations: { type: Array, default: () => [] },
  useBase64: { type: Boolean, default: false }
});

const currentIndex = ref(0);
const displayTitle = ref(props.title);
const slideDirection = ref('next');

onMounted(() => {
  if (!displayTitle.value) {
    const sectionEl = document.querySelector('section:has(.viewer-wrapper)');
    const id = sectionEl?.id;
    if (id) {
      const sectionTitles = {
        header: "Intro",
        info: "The Visual Impaired",
        "gn-diff": "Types of Graphic Novels",
        parts: "Parts of Comics",
        challenges: "Challenges",
        ml: "Machine Learning",
        dl: "Deep Learning"
      };
      displayTitle.value = sectionTitles[id] || "";
    }
  }
});

const prevImage = () => {
  if (currentIndex.value > 0) {
    slideDirection.value = 'prev';
    currentIndex.value--;
  }
};
const nextImage = () => {
  if (currentIndex.value < props.images.length - 1) {
    slideDirection.value = 'next';
    currentIndex.value++;
  }
};
const goToImage = (index) => {
  slideDirection.value = index > currentIndex.value ? 'next' : 'prev';
  currentIndex.value = index;
};
</script>

<template>
  <div v-if="images.length" class="viewer-wrapper">
    <transition name="title-fade" mode="out-in">
      <header class="viewer-title" :key="currentIndex">
        {{ title }}
      </header>
    </transition>

<button
  class="nav-btn left"
  @click="prevImage"
  :disabled="currentIndex === 0"
  aria-label="Previous"
>
  <svg fill="var(--orange)" viewBox="0 0 45.513 45.512" width="36" height="36" xmlns="http://www.w3.org/2000/svg" transform="rotate(180)">
    <path d="M44.275,19.739L30.211,5.675c-0.909-0.909-2.275-1.18-3.463-0.687c-1.188,0.493-1.959,1.654-1.956,2.938l0.015,5.903
      l-21.64,0.054C1.414,13.887-0.004,15.312,0,17.065l0.028,11.522c0.002,0.842,0.338,1.648,0.935,2.242
      s1.405,0.927,2.247,0.925l21.64-0.054l0.014,5.899c0.004,1.286,0.781,2.442,1.971,2.931c1.189,0.487,2.557,0.21,3.46-0.703
      L44.29,25.694C45.926,24.043,45.92,21.381,44.275,19.739z"/>
  </svg>
</button>

<button
  class="nav-btn right"
  @click="nextImage"
  :disabled="currentIndex === images.length - 1"
  aria-label="Next"
>
  <svg fill="var(--orange)" viewBox="0 0 45.513 45.512" width="36" height="36" xmlns="http://www.w3.org/2000/svg">
    <path d="M44.275,19.739L30.211,5.675c-0.909-0.909-2.275-1.18-3.463-0.687c-1.188,0.493-1.959,1.654-1.956,2.938l0.015,5.903
      l-21.64,0.054C1.414,13.887-0.004,15.312,0,17.065l0.028,11.522c0.002,0.842,0.338,1.648,0.935,2.242
      s1.405,0.927,2.247,0.925l21.64-0.054l0.014,5.899c0.004,1.286,0.781,2.442,1.971,2.931c1.189,0.487,2.557,0.21,3.46-0.703
      L44.29,25.694C45.926,24.043,45.92,21.381,44.275,19.739z"/>
  </svg>
</button>

    <transition :name="slideDirection === 'next' ? 'slide-next' : 'slide-prev'" mode="out-in">
      <div :key="currentIndex" class="viewer">
        <div class="explanation-box">
          <h3>{{ images[currentIndex]?.label || "Explanation" }}</h3>
          <p>{{ explanations[currentIndex] || images[currentIndex]?.explanation || "No explanation available." }}</p>
        </div>

        <div class="image-viewer">
          <div class="image-container">
            <img
              :src="useBase64 ? images[currentIndex].base64 : images[currentIndex].src"
              :alt="images[currentIndex].label"
              loading="lazy"
            />
          </div>
        </div>
      </div>
    </transition>

    <div class="dots">
      <span
        v-for="(img, index) in images"
        :key="index"
        :class="{ active: index === currentIndex }"
        @click="goToImage(index)"
      ></span>
    </div>
  </div>
</template>

<style>
:root {
  --orange: #da7434;
  --orange-light: #e28752;
  --bg-light: #f9f9f9;
  --text-dark: #222;
}

.viewer-wrapper {
  position: relative;
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
  padding: 1rem;
  align-items: center;
}

.viewer-title {
  font-size: clamp(1.6rem, 2.2vw, 2.2rem);
  font-weight: 700;
  text-align: center;
  padding: 0.7rem 1.5rem;
  background: linear-gradient(135deg, var(--orange), var(--orange-light));
  color: white;
  border-radius: 14px;
  box-shadow: 0 6px 18px rgba(218, 116, 52, 0.55), inset 0 2px 6px rgba(255, 255, 255, 0.15);
  position: relative;
  overflow: hidden;
  letter-spacing: 0.5px;
  text-transform: uppercase;
}

.viewer-title::after {
  content: "";
  position: absolute;
  bottom: 6px;
  left: 50%;
  transform: translateX(-50%);
  width: 70%;
  height: 3px;
  background: rgba(255, 255, 255, 0.6);
  border-radius: 2px;
}

.viewer {
  display: flex;
  height: 70vh;
  width: 80%;
  max-width: 1200px;
  gap: 1rem;
  background: linear-gradient(135deg, rgba(255,255,255,0.8), rgba(249,249,249,0.6));
  backdrop-filter: blur(12px);
  border-radius: 16px;
  box-shadow: 0 6px 28px rgba(0, 0, 0, 0.12);
  padding: 1rem;
  transform: translateY(-4px);
}

.explanation-box {
  flex: 1;
  display: flex;
  flex-direction: column;
  justify-content: center;
  padding: 2rem;
  overflow: hidden;
}

.explanation-box h3 {
  font-size: clamp(1rem, 1.5vw, 1.3rem);
  margin-bottom: 0.8rem;
  color: var(--orange);
  animation: fadeIn 0.35s ease;
}

.explanation-box p {
  white-space: pre-line;
  font-size: clamp(0.8rem, 1vw, 1rem);
  line-height: 1.4;
  color: var(--text-dark);
  animation: fadeIn 0.35s ease;
}

.image-viewer {
  flex: 1;
  display: flex;
  justify-content: center;
  align-items: center;
}
.image-container img {
  width: 100%;
  height: auto;
  max-width: 90%;
  max-height: 90%;
  object-fit: contain;
  border-radius: 12px;
  box-shadow: 0 4px 20px rgba(218, 116, 52, 0.25);
  animation: fadeIn 0.35s ease;
}

.nav-btn {
  position: absolute;
  top: 50%;
  transform: translateY(-50%) scale(1.05);
  background: transparent;
  color: var(--orange);
  font-size: clamp(1.5rem, 3vw, 2rem);
  padding: 0.6rem;
  border-radius: 50px;
  cursor: pointer;
  transition: all 0.25s ease;
  box-shadow: none;
  z-index: 10;
  display: flex;
  align-items: center;
  justify-content: center;

  border: 2px solid var(--orange);
}

.nav-btn:hover:not(:disabled) {
  border-color: var(--orange-light);
  transform: translateY(-50%) scale(1.3);
  box-shadow: 0 4px 12px rgba(218, 116, 52, 0.3);
}

.nav-btn:active:not(:disabled) {
  transform: translateY(-50%) scale(1.05);
}

.nav-btn:disabled {
  color: rgba(0, 0, 0, 0.1);
  background: rgba(0, 0, 0, 0.05);
  transform: translateY(-50%) scale(1);
  cursor: default;
  border: 2px solid gray;
}

.nav-btn:disabled svg {
  fill: gray;
}
.nav-btn.left { left: 1rem; }
.nav-btn.right { right: 1rem; }

.dots {
  display: flex;
  gap: 12px;
  margin-top: 0.5rem;
}

.dots span {
  width: 24px;
  height: 24px;
  background: rgba(218, 116, 52, 0.4);
  border-radius: 50%;
  cursor: pointer;
  border: 2px solid transparent;
  transition:
    background 0.3s ease,
    transform 0.25s ease,
    box-shadow 0.3s ease,
    border-color 0.3s ease;
}

.dots span:hover {
  background: var(--orange-light);
  border-color: var(--orange);
  transform: scale(1.4);
}

.dots span.active {
  background: var(--orange);
  border-color: var(--orange-light);
  transform: scale(1.6);
}

.slide-next-enter-active, .slide-prev-enter-active,
.slide-next-leave-active, .slide-prev-leave-active {
  transition: all 0.4s ease;
}
.slide-next-enter-from { opacity: 0; transform: translateX(50px); }
.slide-next-leave-to { opacity: 0; transform: translateX(-50px); }
.slide-prev-enter-from { opacity: 0; transform: translateX(-50px); }
.slide-prev-leave-to { opacity: 0; transform: translateX(50px); }

.title-fade-enter-active, .title-fade-leave-active {
  transition: opacity 0.4s ease, transform 0.4s ease;
}
.title-fade-enter-from, .title-fade-leave-to {
  opacity: 0;
  transform: translateY(-10px);
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(5px); }
  to { opacity: 1; transform: translateY(0); }
}

@media (max-width: 768px) {
  .viewer-wrapper {
    justify-content: center;
  }
  .viewer {
    flex-direction: column;
    height: auto;
    width: 100%;
    max-width: 95%;
  }
  .image-viewer {
    order: -1;
    flex: 0 0 auto;
    height: auto;
    padding: 0.5rem 0;
  }
  .image-container img {
    max-height: 30vh;
  }
  .explanation-box {
    flex: 1;
    height: auto;
    padding: 1rem;
  }
  .nav-btn {
    background: transparent !important;
    box-shadow: none !important;
    color: var(--orange);
    padding: 0.4rem;
  }
  .nav-btn.left { left: 0.5rem; }
  .nav-btn.right { right: 0.5rem; }
}
</style>
