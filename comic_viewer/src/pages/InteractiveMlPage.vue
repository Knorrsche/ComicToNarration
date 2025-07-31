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
        <div class="tab-buttons">
          <button @click="activeTab = 'panel'" :class="{ active: activeTab === 'panel' }">Panel Parameters</button>
          <button @click="activeTab = 'bubble'" :class="{ active: activeTab === 'bubble' }">Bubble Parameters</button>
          <button @click="activeTab = 'text'" :class="{ active: activeTab === 'text' }">Text</button>
          <button @click="perfect_setup">Perfect Setup</button>
        </div>

        <div v-if="activeTab === 'text'">
          <h3>Machine Learning in Comics</h3>
          <p>
            Deep learning is a subset of machine learning that uses layered neural networks
            to automatically learn features from large datasets...
          </p>
        </div>

        <div v-else-if="activeTab === 'panel'">
          <h3>Panel Detection Parameters</h3>
          <div class="param-group" v-for="param in panelParams" :key="param.label">
            <label>{{ param.label }}: {{ detectionParams[param.key] }}</label>
            <input type="range" v-bind="param.attrs" v-model="detectionParams[param.key]" />
          </div>
        </div>

        <div v-else-if="activeTab === 'bubble'">
          <h3>Speech Bubble Detection Parameters</h3>
          <div class="param-group" v-for="param in bubbleParams" :key="param.label">
            <label>{{ param.label }}: {{ detectionParams[param.key] }}</label>
            <input type="range" v-bind="param.attrs" v-model="detectionParams[param.key]" />
          </div>
        </div>

        <div class="action-buttons">
          <button :disabled="!imageSrc || loading" @click="applyDetection">Apply Detection</button>
          <button :disabled="!imageSrc" @click="resetImage">Reset</button>
        </div>

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

// Panel parameters bound directly to store values
const panelParams = [
  { label: "Blur Kernel Size", key: "blur", attrs: { min: 1, max: 15, step: 2, type: "range" } },
  { label: "Threshold", key: "threshold", attrs: { min: 0, max: 255, type: "range" } },
  { label: "Morph Kernel Size", key: "morph", attrs: { min: 1, max: 15, step: 2, type: "range" } },
  { label: "Min Panel Size", key: "minSize", attrs: { min: 10, max: 300, type: "range" } }
];

// Bubble parameters bound directly to store values
const bubbleParams = [
  { label: "Bubble Threshold", key: "bubbleThreshold", attrs: { min: 100, max: 255, type: "range" } },
  { label: "Min Circularity", key: "minCircularity", attrs: { min: 0.01, max: 1.0, step: 0.01, type: "range" } },
  { label: "Bubble Min Area", key: "bubbleMin", attrs: { min: 0.0001, max: 1.0, step: 0.0001, type: "range" } },
  { label: "Bubble Max Area", key: "bubbleMax", attrs: { min: 0.0001, max: 1.0, step: 0.0001, type: "range" } }
];

// Set defaults
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

// Apply detection
async function applyDetection() {
  loading.value = true;
  error.value = null;
  try {
    const formData = new FormData();
    const imgResponse = await fetch(imageSrc.value);
    const blob = await imgResponse.blob();
    formData.append("file", blob, "upload.jpg");

    // Always pull latest values directly from detectionParams
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

// Reset image + parameters
function resetImage() {
  processedImageSrc.value = null;
  error.value = null;
  perfect_setup(); // Reset parameters too
}
</script>

<style scoped>
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
  margin-top: 1rem;
  max-width: fit-content;
  margin-left: auto;
  margin-right: auto;
}

.viewer {
  display: flex;
  height: 75vh;
  width: 100%;
}

.image-viewer {
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
}

.image-container img {
  max-width: 100%;
  max-height: 100%;
  object-fit: contain;
}

.explanation-box {
  width: 50%;
  padding: 1rem;
  background: #f9f9f9;
  overflow-y: auto;
}

.tab-buttons {
  display: flex;
  justify-content: space-between;
  flex-wrap: nowrap;
  gap: 4px;
}

.tab-buttons button {
  flex: 1 1 auto;
  font-size: clamp(0.6rem, 1.5vw, 0.9rem);
  padding: 0.3rem 0.4rem;
  white-space: nowrap;
  border-radius: 4px;
  background: #ddd;
  border: 1px solid #ccc;
  cursor: pointer;
  transition: background 0.2s;
}

.tab-buttons button:hover {
  background: #ccc;
}

.tab-buttons button.active {
  background: #007bff;
  color: white;
}

.param-group {
  margin-top: 0.5rem;
}

.action-buttons {
  display: flex;
  gap: 10px;
  margin-top: 1rem;
}

.loading {
  color: #007bff;
}

.error {
  color: red;
}

@media (max-width: 768px) {
  .viewer {
    flex-direction: column;
    height: 100vh;
  }
  .image-viewer {
    width: 100%;
    height: 33%;
  }
  .explanation-box {
    width: 100%;
    height: 67%;
    font-size: clamp(0.8rem, 2vw, 1rem);
    overflow-y: auto;
  }
}
</style>
