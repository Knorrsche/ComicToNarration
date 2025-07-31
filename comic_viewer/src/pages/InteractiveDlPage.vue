<template>
  <div class="outer-container">
    <h1>Deep Learning</h1>
    <div class="content-wrapper">
      <div class="explanation-box">
        <h3>Deep Learning in Comics</h3>
        <p>
          Deep learning is a subset of machine learning that uses layered neural networks (like CNNs or transformers) to automatically learn features from large datasets. Unlike traditional machine learning, which requires handcrafted features (e.g. edge detectors or geometric rules), deep learning models learn directly from raw pixel data — enabling them to identify complex patterns in comic images.
        </p>
        <p>
          In the context of comics, deep learning allows automatic detection and interpretation of panels, speech bubbles, characters, and even emotions or narrative structure. This mimics how humans visually understand and follow stories, enabling smarter comic viewers and tools.
        </p>
      </div>

      <ComicScrollPanel></ComicScrollPanel>
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
.outer-container {
  max-width: 100%;
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  box-sizing: border-box;
  font-family: Arial, sans-serif;
}

.content-wrapper {
  display: flex;
  width: 100%;
  gap: 40px;
  justify-content: center;
  align-items: flex-start;
}

.explanation-box {
  flex: 1 1 50%;
  min-width: 65vh;
  max-width: 65vh;
  height: auto;
  border-radius: 8px;
  box-shadow: 0 0 8px rgba(0, 0, 0, 0.1);
  text-align: left;
  user-select: none;
  color: #333;
  font-weight: 600;
  display: flex;
  flex-direction: column;
  justify-content: center;
}

.explanation-box p {
  font-size: 1rem;
  color: #555;
  line-height: 1.4;
  margin-bottom: 10px;
}

.image-wrapper img {
  width: 100%;
  height: auto;
  object-fit: contain;
  border-radius: 6px;
  box-shadow: 0 0 12px rgba(0, 0, 0, 0.2);
  user-select: none;
  display: block;
}

@media (max-width: 768px) {
  .content-wrapper {
    flex-direction: column;
    gap: 20px;
    align-items: center;
  }

  .explanation-box {
    max-width: 100%;
    min-width: auto;
    order: 1;
  }

  .content-wrapper > :last-child {
    order: 2;
    width: 100%;
  }

  .content-wrapper > :last-child {
    max-height: 60vh;
    overflow-y: auto;
  }
}
</style>
