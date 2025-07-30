<script setup>
import { ref } from 'vue';

const props = defineProps({
  images: {
    type: Array,
    required: true
  },
  explanations: {
    type: Array,
    default: () => []
  },
  useBase64: {
    type: Boolean,
    default: false
  }
});

const currentIndex = ref(0);

const prevImage = () => {
  if (currentIndex.value > 0) currentIndex.value--;
};

const nextImage = () => {
  if (currentIndex.value < props.images.length - 1) currentIndex.value++;
};
</script>

<template>
  <div v-if="images.length" class="viewer">
    <!-- Left: Explanation -->
    <div class="explanation-box">
      <h3>{{ images[currentIndex]?.label || "Explanation" }}</h3>
      <p>{{ explanations[currentIndex] || images[currentIndex]?.explanation || "No explanation available." }}</p>
    </div>

    <!-- Right: Image with smaller overlay buttons -->
    <div class="image-viewer">
      <div class="image-container">
        <img
          :src="useBase64 ? images[currentIndex].base64 : images[currentIndex].src"
          :alt="images[currentIndex].label"
          loading="lazy"
        />

        <!-- Floating Small Buttons -->
        <button
          class="image-nav-btn left"
          @click="prevImage"
          :disabled="currentIndex === 0"
          aria-label="Previous Image"
        >
          ◀
        </button>

        <button
          class="image-nav-btn right"
          @click="nextImage"
          :disabled="currentIndex === images.length - 1"
          aria-label="Next Image"
        >
          ▶
        </button>
      </div>
    </div>
  </div>
</template>

<style>
.viewer {
  display: flex;
  height: 75vh;
  width: 100%;
  overflow: hidden;
}

.explanation-box {
  width: 50%;
  display: flex;
  flex-direction: column;
  padding: 1.5rem;
  background: #f9f9f9;
  border: 2px solid #ca2020;
  overflow-y: auto;
}

.image-viewer {
  position: relative;
  width: 50%;
  display: flex;
  flex-direction: column;
  border: 2px solid #ca2020;
}

.image-container {
  flex: 1;
  display: flex;
  justify-content: center;
  align-items: center;
  overflow: hidden;
  position: relative;
}

.image-container img {
  max-width: 100%;
  max-height: 100%;
  object-fit: contain;
}

/* Smaller overlay buttons with responsive font size */
.image-nav-btn {
  position: absolute;
  top: 50%;
  transform: translateY(-50%);
  background: rgba(0, 0, 0, 0.4);
  color: white;
  font-size: clamp(1.2rem, 2vw, 2rem); /* scales with screen size */
  padding: 0.5rem 0.8rem;
  border: none;
  border-radius: 50%;
  cursor: pointer;
  transition: background 0.2s ease;
}

.image-nav-btn:hover {
  background: rgba(0, 0, 0, 0.6);
}

.image-nav-btn:disabled {
  background: rgba(0, 0, 0, 0.2);
  cursor: default;
}

.image-nav-btn.left {
  left: 10px;
}

.image-nav-btn.right {
  right: 10px;
}

/* Mobile adjustments */
@media (max-width: 768px) {
  .viewer {
    flex-direction: column;
    height: 100vh;
  }

  .image-viewer {
    order: -1;
    width: 100%;
    height: 60vh;
  }

  .explanation-box {
    width: 100%;
    height: 40vh;
    font-size: 0.95rem;
    padding: 1rem;
    overflow-y: auto;
  }

  .image-nav-btn {
    font-size: clamp(1.5rem, 6vw, 2.5rem);
    padding: 0.4rem 0.7rem;
  }
}
</style>
