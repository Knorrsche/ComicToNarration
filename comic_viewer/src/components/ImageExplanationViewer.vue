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

onMounted(() => {
  if (!displayTitle.value) {
    // get the section id from the closest parent section in DOM
    const sectionEl = document.querySelector('section:has(.viewer-wrapper)');
    const id = sectionEl?.id;
    if (id) {
      // Map section ids to titles here
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

const prevImage = () => { if (currentIndex.value > 0) currentIndex.value--; };
const nextImage = () => { if (currentIndex.value < props.images.length - 1) currentIndex.value++; };
</script>

<template>
  <div v-if="images.length" class="viewer-wrapper">
    <!-- Section Title -->
    <header class="viewer-title" v-if="title">
      {{ title }}
    </header>

    <div class="viewer">
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
  </div>
</template>

<style>
.viewer-wrapper {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.viewer-title {
  font-size: clamp(1.5rem, 2vw, 2rem);
  font-weight: bold;
  text-align: center;
  padding: 0.5rem 1rem;
  background: rgba(218, 116, 52, 0.85);
  color: white;
  border-radius: 8px;
  margin-top: 3rem;
  margin-left: auto;
  margin-right: auto;
  max-width: fit-content;
  box-shadow: 0 2px 6px rgba(0,0,0,0.2);
}

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

.image-nav-btn {
  position: absolute;
  top: 50%;
  transform: translateY(-50%);
  background: rgba(0, 0, 0, 0.4);
  color: white;
  font-size: clamp(1.2rem, 2vw, 2rem);
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

/* Mobile Layout Fix */
@media (max-width: 768px) {
  .viewer {
    flex-direction: column;
    height: 100vh;
    width: 100%; /* fix cut-off */
    overflow-x: hidden;
  }

  .image-viewer {
    order: -1;
    width: 100%;
    height: 33vh;
    border: none; /* remove border */
    padding: 0;
    margin: 0;
  }

  .image-container {
    width: 100%;
    height: 100%;
  }

  .image-container img {
    width: 100%;
    height: auto;
    max-height: 100%;
    object-fit: contain;
    display: block; /* prevent overflow gaps */
  }

  .explanation-box {
    width: 100%;
    height: 67vh;
    font-size: 0.9rem;
    padding: 0;
    margin: 0;
    overflow-y: auto;
    box-sizing: border-box;
  }

  .image-nav-btn {
    font-size: clamp(1rem, 5vw, 1.8rem);
    padding: 0.3rem 0.6rem;
  }

  .explanation-box h3 {
    font-size: 1rem;
    margin-bottom: 0.4rem;
  }

  .explanation-box p {
    font-size: 0.85rem;
    line-height: 1.3;
  }
}

@media (max-width: 768px) {
  .viewer-title {
    font-size: 1.2rem;
    padding: 0.4rem 0.8rem;
    border-radius: 0;
    background: rgba(218, 116, 52, 0.85);
    position: sticky;
    top: 0;
    z-index: 10;
  }
}
</style>
