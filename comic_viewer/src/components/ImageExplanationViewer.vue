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
    <div class="explanation-box">
      <h3>{{ images[currentIndex]?.label || "Explanation" }}</h3>
      <p>{{ explanations[currentIndex] || images[currentIndex]?.explanation || "No explanation available." }}</p>
    </div>

    <div class="image-viewer">
      <div class="buttons-row">
        <button
          class="nav-button"
          @click="prevImage"
          :disabled="currentIndex === 0"
          aria-label="Previous Image"
        >
          ◀ Prev
        </button>

        <button
          class="nav-button"
          @click="nextImage"
          :disabled="currentIndex === images.length - 1"
          aria-label="Next Image"
        >
          Next ▶
        </button>
      </div>

      <div class="image-container">
        <img
          :src="useBase64 ? images[currentIndex].base64 : images[currentIndex].src"
          :alt="images[currentIndex].label"
          loading="lazy"
        />
      </div>
    </div>
  </div>
</template>

<style>
.viewer {
  display: flex;
  height: 75vh; /* fit exactly in the viewport */
  width: 100%;
  overflow: hidden;
}

.explanation-box {
  width: 50%;
  display: flex;
  flex-direction: column;
  padding: 2rem;
  background: #f9f9f9;
  border: 2px solid #ca2020;
  overflow-y: auto; /* scroll if too long */
}

.image-viewer {
  width: 50%;
  display: flex;
  flex-direction: column;
  border: 2px solid #ca2020;
}

.buttons-row {
  flex-shrink: 0; /* buttons keep size */
  display: flex;
  justify-content: space-between;
  gap: 1rem;
  padding: 0.5rem;
}

.nav-button {
  flex: 1;
  background-color: #007bff;
  color: white;
  border: none;
  padding: 0.6rem 0;
  font-size: clamp(1rem, 1.8vw, 1.3rem);
  cursor: pointer;
  border-radius: 5px;
}
.nav-button:disabled {
  background-color: #ccc;
  cursor: not-allowed;
}

.image-container {
  flex: 1; /* fills remaining space */
  display: flex;
  justify-content: center;
  align-items: center;
  overflow: hidden;
}

.image-container img {
  max-width: 100%;
  max-height: 100%;
  object-fit: contain;
}

/* Mobile */
@media (max-width: 768px) {
  .viewer {
    flex-direction: column;
    height: auto;
  }
  .explanation-box,
  .image-viewer {
    width: 100%;
    height: auto;
  }
}
</style>
