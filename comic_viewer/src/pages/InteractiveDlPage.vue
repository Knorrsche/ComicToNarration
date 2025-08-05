<template>
  <div class="outer-container">
    <h1 class="section-title">Deep Learning</h1>
    <div class="content-wrapper">
      <div class="explanation-box">
        <h3>Deep Learning in Comics</h3>
        <p>
          Deep learning is a subset of machine learning that uses layered neural networks
          (like CNNs or transformers) to automatically learn features from large datasets.
          Unlike traditional machine learning, which requires handcrafted features
          (e.g. edge detectors or geometric rules), deep learning models learn directly from
          raw pixel data — enabling them to identify complex patterns in comic images.
        </p>
        <p>
          In the context of comics, deep learning allows automatic detection and interpretation
          of panels, speech bubbles, characters, and even emotions or narrative structure.
          This mimics how humans visually understand and follow stories, enabling smarter
          comic viewers and tools.
        </p>
      </div>

      <ComicScrollPanel />
    </div>
  </div>
</template>

<script setup>
import ComicScrollPanel from "../components/ComicScrollPanel.vue";

const props = defineProps({
  title: {
    type: String,
    required: true
  }
});
</script>

<style scoped>
:root {
  --orange: #da7434;
  --orange-hover: #c45d1f;
  --bg-blur: rgba(255, 255, 255, 0.75);
}

.outer-container {
  max-width: 100%;
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  gap: 2rem;
  padding: 2rem;
  box-sizing: border-box;
  font-family: "Inter", "Segoe UI", Tahoma, sans-serif;
}

.section-title {
  font-size: clamp(1.8rem, 4vw, 2.4rem);
  font-weight: bold;
  text-align: center;
  color: var(--orange);
}

.content-wrapper {
  display: flex;
  width: 100%;
  gap: 2rem;
  justify-content: center;
  align-items: flex-start;
  flex-wrap: wrap;
}

/* Glassmorphism Explanation Box */
.explanation-box {
  flex: 1 1 50%;
  min-width: 300px;
  max-width: 650px;
  padding: 2rem;
  background: var(--bg-blur);
  backdrop-filter: blur(12px);
  border-radius: 16px;
  box-shadow: 0 4px 25px rgba(0, 0, 0, 0.08);
  color: #333;
  font-weight: 500;
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.explanation-box h3 {
  font-size: 1.4rem;
  font-weight: 600;
  color: var(--orange);
}

.explanation-box p {
  font-size: 1rem;
  color: #555;
  line-height: 1.6;
}

/* Mobile Layout */
@media (max-width: 768px) {
  .content-wrapper {
    flex-direction: column;
    align-items: center;
  }

  .explanation-box {
    width: 100%;
    padding: 1.5rem;
  }
}
</style>
