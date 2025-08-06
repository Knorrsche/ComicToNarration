<template>
  <div class="viewer-wrapper">
    <!-- Title -->
    <header class="viewer-title">
      {{ title }}
    </header>

    <!-- Main Content -->
    <div class="viewer">
      <!-- Explanation -->
      <div class="explanation-box">
        <h3>Deep Learning in Comics</h3>
        <p>
          Deep learning is a branch of artificial intelligence that uses multi-layered
          neural networks, such as convolutional neural networks (CNNs) or transformers,
          to automatically discover visual patterns from raw data. Instead of relying on
          hand-tuned rules like edge detectors or geometric shape finders, these models
          learn directly from pixel values, building their own understanding of what
          panels, speech bubbles, or characters look like.
        </p>
        <p>
          In comics, this means deep learning can detect and classify panels, identify
          speech bubbles, track characters, and even infer emotions or scene context.
          Because the models learn from large and diverse datasets, they are far more
          adaptable to different art styles, unconventional layouts, and creative designs
          than traditional rule-based methods.
        </p>
        <p>
          You can explore this in action with the interactive viewer, adjust parameters,
          apply detection, and compare results to see how automated understanding of
          comics can be both powerful and flexible in capturing the richness of the medium.
          You can also compare the outputs of this deep learning model with the rule-based
          detections you configured in the previous section to better understand the strengths
          and limitations of each approach.
        </p>
      </div>

      <!-- Comic Panel List -->
      <div class="image-viewer">
        <ComicScrollPanel />
      </div>
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
  --orange-light: #e28752;
  --bg-light: #f9f9f9;
  --text-dark: #222;
}

/* Wrapper matches viewer component */
.viewer-wrapper {
  position: relative;
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
  padding: 1rem;
  align-items: center;
}

/* Gradient Title Bar */
.viewer-title {
  font-size: clamp(1.6rem, 2.2vw, 2.2rem);
  font-weight: 700;
  text-align: center;
  padding: 0.7rem 1.5rem;
  background: linear-gradient(135deg, var(--orange), var(--orange-light));
  color: white;
  border-radius: 14px;
  box-shadow: 0 6px 18px rgba(218, 116, 52, 0.55), inset 0 2px 6px rgba(255, 255, 255, 0.15);
  letter-spacing: 0.5px;
  text-transform: uppercase;
  position: relative;
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

/* Main Glassmorphic Container */
.viewer {
  display: flex;
  width: 80%;
  max-width: 1200px;
  gap: 1rem;
  background: linear-gradient(135deg, rgba(255,255,255,0.8), rgba(249,249,249,0.6));
  backdrop-filter: blur(12px);
  border-radius: 16px;
  box-shadow: 0 6px 28px rgba(0, 0, 0, 0.12);
  padding: 1rem;
  align-items: stretch;
  max-height: 75vh;
}

/* Explanation Box */
.explanation-box {
  flex: 1;
  display: flex;
  flex-direction: column;
  justify-content: center;
  padding: 2rem;
  overflow: hidden; /* remove scrollbar */
}

.explanation-box h3 {
  font-size: clamp(1rem, 1.5vw, 1.3rem); /* shrink title if needed */
  margin-bottom: 0.8rem;
  color: var(--orange);
}
.explanation-box p {
  font-size: clamp(0.8rem, 1vw, 1rem); /* shrink text instead of scrolling */
  line-height: 1.4;
  color: var(--text-dark);
  white-space: pre-line;
}

/* Comic Scroll Panel Wrapper */
.image-viewer {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  justify-content: flex-start;
  overflow-y: auto;
  max-height: 100%;
  padding-top: 0.5rem;
}

/* Orange scrollbar for comic list */
.image-viewer::-webkit-scrollbar {
  width: 8px;
}
.image-viewer::-webkit-scrollbar-thumb {
  background-color: var(--orange);
  border-radius: 4px;
}
.image-viewer::-webkit-scrollbar-track {
  background: transparent;
}

/* Ensure Select Comic text inside ComicScrollPanel is fully visible */
.image-viewer :deep(select) {
  max-width: 100%;
  white-space: normal;
}

/* Mobile Layout */
@media (max-width: 768px) {
  .viewer {
    flex-direction: column;
    width: 100%;
    max-width: 95%;
    max-height: none;
  }
  .image-viewer {
    order: -1;
    max-height: none;
  }
}
</style>
