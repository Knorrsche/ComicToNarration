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
const goToImage = (index) => {
  slideDirection.value = index > currentIndex.value ? 'next' : 'prev';
  currentIndex.value = index;
};
</script>

<template>
  <div v-if="images.length" class="viewer-wrapper">
    <!-- Middle Title with transition -->
    <transition name="title-fade" mode="out-in">
      <header class="viewer-title" :key="currentIndex">
        {{ title }}
      </header>
    </transition>

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

    <!-- Pagination Dots -->
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

/* Upgraded Viewer Title - Always Hover Style */
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
  width: 70%; /* Always expanded underline */
  height: 3px;
  background: rgba(255, 255, 255, 0.6);
  border-radius: 2px;
}

/* Viewer Layout - Always Hover Style */
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
  transform: translateY(-4px); /* Always lifted */
}

/* Explanation Box */
.explanation-box {
  flex: 1;
  display: flex;
  flex-direction: column;
  justify-content: center;
  padding: 2rem;
  overflow: hidden; /* remove scrollbars */
}

.explanation-box h3 {
  font-size: clamp(1rem, 1.5vw, 1.3rem);
  margin-bottom: 0.8rem;
  color: var(--orange);
  animation: fadeIn 0.35s ease;
}

.explanation-box p {
  white-space: pre-line;
  font-size: clamp(0.8rem, 1vw, 1rem); /* scales text if space is limited */
  line-height: 1.4;
  color: var(--text-dark);
  animation: fadeIn 0.35s ease;
}

/* Image Viewer */
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
  box-shadow: 0 4px 20px rgba(218, 116, 52, 0.25); /* Slightly stronger */
  animation: fadeIn 0.35s ease;
}

/* Navigation Buttons - Always Hover Style */
.nav-btn {
  position: absolute;
  top: 50%;
  transform: translateY(-50%) scale(1.05);
  background: #c45d1f;
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
.nav-btn:disabled {
  background: rgba(0,0,0,0.2);
  transform: translateY(-50%) scale(1);
  cursor: default;
}
.nav-btn.left { left: 1rem; }
.nav-btn.right { right: 1rem; }

/* Pagination Dots */
.dots {
  display: flex;
  gap: 8px;
  margin-top: 0.5rem;
}
.dots span {
  width: 12px;
  height: 12px;
  background: rgba(218, 116, 52, 0.4);
  border-radius: 50%;
  cursor: pointer;
  transition: background 0.3s ease, transform 0.25s ease;
}
.dots span:hover {
  background: rgba(218, 116, 52, 0.7);
  transform: scale(1.2);
}
.dots span.active {
  background: var(--orange);
  transform: scale(1.3);
}

/* Animations */
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

/* Mobile Layout */
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
    order: -1; /* Image above explanation */
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
  .nav-btn.left { left: 0.5rem; }
  .nav-btn.right { right: 0.5rem; }
}
</style>
