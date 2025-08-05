<template>
  <div v-if="imageSrc" class="viewer-wrapper">
    <!-- Title -->
    <header class="viewer-title">
      Interactive Comic Panel & Speech Bubble Detection
    </header>

    <div class="viewer">
      <!-- Image Section -->
      <div class="image-viewer">
        <div class="image-container">
          <img
            :src="processedImageSrc || imageSrc"
            alt="Comic"
          />
        </div>
      </div>

      <!-- Controls / Explanation -->
      <div class="explanation-box">
        <!-- Tab Buttons -->
        <div class="tab-buttons">
          <button @click="activeTab = 'panel'" :class="{ active: activeTab === 'panel' }">Panel Parameters</button>
          <button @click="activeTab = 'bubble'" :class="{ active: activeTab === 'bubble' }">Bubble Parameters</button>
          <button @click="activeTab = 'text'" :class="{ active: activeTab === 'text' }">Text</button>
          <button class="secondary" @click="perfect_setup">Perfect Setup</button>
        </div>

        <!-- Text Tab -->
        <div v-if="activeTab === 'text'" class="tab-content">
          <h3>Machine Learning in Comics</h3>
          <p>
            Deep learning is a subset of machine learning that uses layered neural networks
            to automatically learn features from large datasets. In the context of comics,
            these models can detect panels, speech bubbles, and even text regions to enhance
            accessibility and automate processing.
          </p>
        </div>

        <!-- Panel Parameters -->
        <div v-else-if="activeTab === 'panel'" class="tab-content">
          <h3>Panel Detection Parameters</h3>
          <div class="param-group" v-for="param in panelParams" :key="param.label">
            <label>{{ param.label }}: {{ detectionParams[param.key] }}</label>
            <input type="range" v-bind="param.attrs" v-model="detectionParams[param.key]" />
          </div>
        </div>

        <!-- Bubble Parameters -->
        <div v-else-if="activeTab === 'bubble'" class="tab-content">
          <h3>Speech Bubble Detection Parameters</h3>
          <div class="param-group" v-for="param in bubbleParams" :key="param.label">
            <label>{{ param.label }}: {{ detectionParams[param.key] }}</label>
            <input type="range" v-bind="param.attrs" v-model="detectionParams[param.key]" />
          </div>
        </div>

        <!-- Action Buttons -->
        <div class="action-buttons">
          <button class="primary" :disabled="!imageSrc || loading" @click="applyDetection">Apply Detection</button>
          <button class="secondary" :disabled="!imageSrc" @click="resetImage">Reset</button>
        </div>

        <!-- Status -->
        <div v-if="loading" class="loading">Processing image, please wait...</div>
        <div v-if="error" class="error">{{ error }}</div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from "vue";
import { detectionParams } from "../stores/detectionParams";
import ComicImage from "../assets/Normal.jpg";

const imageSrc = ref(ComicImage);
const processedImageSrc = ref(null);
const loading = ref(false);
const error = ref(null);

const activeTab = ref("text");

// Panel parameters
const panelParams = [
  { label: "Blur Kernel Size", key: "blur", attrs: { min: 1, max: 15, step: 2, type: "range" } },
  { label: "Threshold", key: "threshold", attrs: { min: 0, max: 255, type: "range" } },
  { label: "Morph Kernel Size", key: "morph", attrs: { min: 1, max: 15, step: 2, type: "range" } },
  { label: "Min Panel Size", key: "minSize", attrs: { min: 10, max: 300, type: "range" } }
];

// Bubble parameters
const bubbleParams = [
  { label: "Bubble Threshold", key: "bubbleThreshold", attrs: { min: 100, max: 255, type: "range" } },
  { label: "Min Circularity", key: "minCircularity", attrs: { min: 0.01, max: 1.0, step: 0.01, type: "range" } },
  { label: "Bubble Min Area", key: "bubbleMin", attrs: { min: 0.0001, max: 1.0, step: 0.0001, type: "range" } },
  { label: "Bubble Max Area", key: "bubbleMax", attrs: { min: 0.0001, max: 1.0, step: 0.0001, type: "range" } }
];

function perfect_setup() {
  detectionParams.threshold = 100;
  detectionParams.blur = 5;
  detectionParams.morph = 5;
  detectionParams.minSize = 60;
  detectionParams.bubbleThreshold = 102;
  detectionParams.bubbleMin = 0.0028;
  detectionParams.bubbleMax = 0.1;
  detectionParams.minCircularity = 0.31;
}

async function applyDetection() {
  loading.value = true;
  error.value = null;
  try {
    const formData = new FormData();
    formData.append("comic", "static");
    formData.append("page", "AlleyOop.png");

    formData.append("blur", detectionParams.blur);
    formData.append("threshold", detectionParams.threshold);
    formData.append("morph", detectionParams.morph);
    formData.append("min_size", detectionParams.minSize);
    formData.append("bubble_thresh", detectionParams.bubbleThreshold);
    formData.append("bubble_min_area", detectionParams.bubbleMin);
    formData.append("bubble_max_area", detectionParams.bubbleMax);
    formData.append("min_circularity", detectionParams.minCircularity);

    const serverRes = await fetch("http://localhost:8000/api/process", {
      method: "POST",
      body: formData
    });

    if (!serverRes.ok) throw new Error(`Server error: ${serverRes.statusText}`);

    const blobResult = await serverRes.blob();
    processedImageSrc.value = URL.createObjectURL(blobResult);
  } catch (err) {
    error.value = err.message || "Image processing failed";
  } finally {
    loading.value = false;
  }
}

function resetImage() {
  processedImageSrc.value = null;
  error.value = null;
  perfect_setup();
}
</script>

<style scoped>
:root {
  --orange: #da7434;
  --orange-hover: #c45d1f;
  --bg-blur: rgba(255, 255, 255, 0.75);
}

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
  background: var(--orange);
  color: white;
  border-radius: 12px;
  margin-top: 1rem;
  box-shadow: 0 3px 10px rgba(0,0,0,0.15);
}

.viewer {
  display: flex;
  height: 75vh;
  width: 100%;
  gap: 1rem;
}

.image-viewer {
  width: 50%;
  display: flex;
  flex-direction: column;
  background: var(--bg-blur);
  backdrop-filter: blur(10px);
  border-radius: 16px;
  box-shadow: 0 4px 25px rgba(0, 0, 0, 0.08);
  overflow: hidden;
}

.image-container {
  flex: 1;
  display: flex;
  justify-content: center;
  align-items: center;
}

.image-container img {
  width: 80%;
  height: 80%;
  object-fit: contain;
  border-radius: 12px;
}

.explanation-box {
  width: 50%;
  padding: 1.2rem;
  background: var(--bg-blur);
  backdrop-filter: blur(10px);
  border-radius: 16px;
  box-shadow: 0 4px 25px rgba(0, 0, 0, 0.08);
  overflow-y: auto;
  display: flex;
  flex-direction: column;
}

.tab-buttons {
  display: flex;
  gap: 0.5rem;
  margin-bottom: 1rem;
  flex-wrap: wrap;
}

.tab-buttons button {
  flex: 1;
  padding: 0.4rem 0.6rem;
  font-size: 0.85rem;
  border: none;
  border-radius: 6px;
  background: #ddd;
  cursor: pointer;
  transition: all 0.2s ease;
}

.tab-buttons button:hover {
  background: #ccc;
}

.tab-buttons button.active {
  background: var(--orange);
  color: white;
}

.tab-buttons button.secondary {
  background: white;
  border: 1px solid var(--orange);
  color: var(--orange);
}

.tab-buttons button.secondary:hover {
  background: var(--orange-hover);
  color: white;
}

.param-group {
  margin-top: 0.5rem;
}

.param-group label {
  font-size: 0.9rem;
  display: block;
  margin-bottom: 0.2rem;
}

.param-group input {
  width: 100%;
}

.action-buttons {
  display: flex;
  gap: 10px;
  margin-top: 1rem;
}

button.primary {
  background: var(--orange);
  color: white;
  border: none;
  padding: 0.5rem 1rem;
  border-radius: 6px;
  cursor: pointer;
  transition: background 0.2s ease;
}

button.primary:hover {
  background: var(--orange-hover);
}

button.secondary {
  background: white;
  border: 1px solid var(--orange);
  color: var(--orange);
  padding: 0.5rem 1rem;
  border-radius: 6px;
  cursor: pointer;
  transition: all 0.2s ease;
}

button.secondary:hover {
  background: var(--orange-hover);
  color: white;
}

.loading {
  color: var(--orange);
  margin-top: 0.5rem;
}

.error {
  color: red;
  margin-top: 0.5rem;
}

@media (max-width: 768px) {
  .viewer {
    flex-direction: column;
    height: auto;
  }
  .image-viewer {
    width: 100%;
    height: 40vh;
  }
  .explanation-box {
    width: 100%;
    height: auto;
  }
}
</style>
