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
        <div class="caption">{{ images[currentIndex].label }}</div>
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
  flex-wrap: nowrap;
  align-items: stretch; /* Ensures children match height */
  justify-content: center;
  gap: 2rem;
  min-height: 60vh;
  padding: 1rem;
  box-sizing: border-box;
}

.explanation-box {
  height: 50vh;
  flex: 1 1 600px;
  max-width: 600px;
  display: flex;
  flex-direction: column;
  justify-content: flex-start;
}


.image-viewer {
  height: 65vh;
  flex: 1 1 600px;
  max-width: 600px;
  display: flex;
  flex-direction: column;
  justify-content: flex-start;
}

.explanation-box h3 {
  font-family: Tahoma, sans-serif;
  margin-bottom: 0.75rem;
  font-size: clamp(1.2rem, 2vw, 1.5rem);
  color: #444;
}

.explanation-box p {
  white-space: pre-line;
  font-family: Tahoma, sans-serif;
  font-size: clamp(1.2rem, 1.5vw, 1.1rem);
  color: #555;
  line-height: 1.5;
}

.image-viewer {
  flex: 1 1 600px;
  max-width: 600px;
  display: flex;
  flex-direction: column;
  align-items: center;
  user-select: none;
}

.buttons-row {
  width: 100%;
  display: flex;
  justify-content: space-between;
  margin-bottom: 0.75rem;
  gap: 1rem;
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
  user-select: none;
  transition: background-color 0.25s ease;
}

.nav-button:hover:not(:disabled),
.nav-button:focus:not(:disabled) {
  background-color: #0056b3;
  outline: none;
}

.nav-button:disabled {
  background-color: #ccc;
  cursor: not-allowed;
  opacity: 0.6;
}

.image-container {
  flex: 1;
  width: 80%;
  height: 80%;
  border-radius: 6px;

  overflow: hidden;
  display: flex;
  flex-direction: column;
  align-items: center;
  padding-top: 2rem;
  box-sizing: border-box;
}

.caption {
  position: absolute;
  top: 0.5rem;
  width: 100%;
  font-weight: 600;
  font-size: clamp(1rem, 1.8vw, 1.2rem);
  color: #333;
  text-align: center;
  user-select: none;
  pointer-events: none;
  z-index: 2;
}

.image-container img {
    box-shadow: 0 0 12px rgba(0, 0, 0, 0.2);
  max-width: 100%;
  max-height: calc(100% - 2.5rem);
  object-fit: fill;
  border-radius: 6px;
  display: block;
  margin: 0 auto;
  user-select: none;
  z-index: 1;
}

/* Responsive */

@media (max-width: 768px) {
  .viewer {
    flex-wrap: wrap;
  }
  .image-viewer,
  .explanation-box {
    max-width: 100%;
    flex-basis: 100%;
  }
  .image-container {
    height: 300px;
  }
}

@media (max-width: 480px) {
  .nav-button {
    font-size: 1.1rem;
    padding: 0.5rem 0;
  }

  .image-container {
    height: 250px;
  }
}
</style>
