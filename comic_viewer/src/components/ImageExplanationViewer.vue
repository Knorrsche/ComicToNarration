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
const slideDirection = ref('next'); // 'next' or 'prev'

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
</script>

<template>
  <div v-if="images.length" class="viewer-wrapper">
    <!-- Middle Title -->
    <header class="viewer-title">
      {{ title }}
    </header>

    <!-- Navigation Buttons -->
    <button
      class="nav-btn left"
      @click="prevImage"
      :disabled="currentIndex === 0"
      aria-label="Previous"
    >
      ◀
    </button>

    <button
      class="nav-btn right"
      @click="nextImage"
      :disabled="currentIndex === images.length - 1"
      aria-label="Next"
    >
      ▶
    </button>

    <!-- Viewer Content with transition -->
    <transition :name="slideDirection === 'next' ? 'slide-next' : 'slide-prev'" mode="out-in">
      <div :key="currentIndex" class="viewer">
        <!-- Explanation -->
        <div class="explanation-box">
          <h3>{{ images[currentIndex]?.label || "Explanation" }}</h3>
          <p>{{ explanations[currentIndex] || images[currentIndex]?.explanation || "No explanation available." }}</p>
        </div>

        <!-- Image -->
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
  </div>
</template>

<style>
:root {
  --orange: #da7434;
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
  font-size: clamp(1.5rem, 2vw, 2rem);
  font-weight: bold;
  text-align: center;
  padding: 0.6rem 1.2rem;
  background: var(--orange);
  color: white;
  border-radius: 12px;
  box-shadow: 0 3px 10px rgba(0,0,0,0.15);
}

/* Viewer Layout */
.viewer {
  display: flex;
  height: 70vh;
  width: 80%;
  max-width: 1200px;
  gap: 1rem;
  background: rgba(255, 255, 255, 0.7);
  backdrop-filter: blur(12px);
  border-radius: 16px;
  box-shadow: 0 4px 25px rgba(0, 0, 0, 0.05);
  padding: 1rem;
}

/* Explanation Box */
.explanation-box {
  width: 50%;
  display: flex;
  flex-direction: column;
  justify-content: center;
  padding: 2rem;
  overflow-y: auto;
}

.explanation-box h3 {
  font-size: 1.3rem;
  margin-bottom: 0.8rem;
  color: var(--orange);
}

.explanation-box p {
  white-space: pre-line;
  font-size: 1rem;
  line-height: 1.6;
  color: var(--text-dark);
}

/* Image Viewer */
.image-viewer {
  width: 50%;
  display: flex;
  justify-content: center;
  align-items: center;
}

.image-container img {
  width: 80%;
  height: 80%;
  max-width: 80%;
  max-height: 80%;
  object-fit: contain;
  border-radius: 12px;
}

/* Navigation Buttons on full height sides */
.nav-btn {
  position: absolute;
  top: 50%;
  transform: translateY(-50%);
  background: var(--orange);
  color: white;
  font-size: clamp(1.5rem, 3vw, 2rem);
  padding: 0.6rem 1rem;
  border: none;
  border-radius: 50%;
  cursor: pointer;
  transition: all 0.2s ease;
  box-shadow: 0 3px 6px rgba(0,0,0,0.15);
  z-index: 10;
}

.nav-btn:hover {
  background: #c45d1f;
  transform: translateY(-50%) scale(1.05);
}

.nav-btn:disabled {
  background: rgba(0,0,0,0.2);
  cursor: default;
}

.nav-btn.left { left: 1rem; }
.nav-btn.right { right: 1rem; }

/* Slide Animations */
.slide-next-enter-active, .slide-prev-enter-active,
.slide-next-leave-active, .slide-prev-leave-active {
  transition: all 0.4s ease;
}

.slide-next-enter-from {
  opacity: 0;
  transform: translateX(50px);
}
.slide-next-leave-to {
  opacity: 0;
  transform: translateX(-50px);
}

.slide-prev-enter-from {
  opacity: 0;
  transform: translateX(-50px);
}
.slide-prev-leave-to {
  opacity: 0;
  transform: translateX(50px);
}

/* Mobile Layout */
@media (max-width: 768px) {
  .viewer {
    flex-direction: column;
    height: auto;
    width: 100%;
  }

  .explanation-box {
    width: 100%;
    padding: 1.2rem;
  }

  .image-viewer {
    width: 100%;
    height: 40vh;
  }

  .nav-btn.left { left: 0.5rem; }
  .nav-btn.right { right: 0.5rem; }
}
</style>
