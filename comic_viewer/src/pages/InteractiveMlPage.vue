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
            <label>{{ param.label }}: {{ param.model }}</label>
            <input type="range" v-bind="param.attrs" v-model="param.model" />
          </div>
        </div>

        <div v-else-if="activeTab === 'bubble'">
          <h3>Speech Bubble Detection Parameters</h3>
          <div class="param-group" v-for="param in bubbleParams" :key="param.label">
            <label>{{ param.label }}: {{ param.model }}</label>
            <input type="range" v-bind="param.attrs" v-model="param.model" />
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
import { ref, watch } from "vue";
import { detectionParams } from "../stores/detectionParams";
import ComicImage from "../assets/Normal.jpg";

const imageSrc = ref(ComicImage);
const processedImageSrc = ref(null);
const loading = ref(false);
const error = ref(null);

const blur = ref(detectionParams.blur);
const threshold = ref(detectionParams.threshold);
const morph = ref(detectionParams.morph);
const minSize = ref(detectionParams.minSize);
const bubbleThreshold = ref(detectionParams.bubbleThreshold);
const bubbleMin = ref(detectionParams.bubbleMin);
const bubbleMax = ref(detectionParams.bubbleMax);
const minCircularity = ref(detectionParams.minCircularity);

const activeTab = ref("text");

const panelParams = [
  { label: "Blur Kernel Size", model: blur, attrs: { min: 1, max: 15, step: 2, type: "range" } },
  { label: "Threshold", model: threshold, attrs: { min: 0, max: 255, type: "range" } },
  { label: "Morph Kernel Size", model: morph, attrs: { min: 1, max: 15, step: 2, type: "range" } },
  { label: "Min Panel Size", model: minSize, attrs: { min: 10, max: 300, type: "range" } }
];

const bubbleParams = [
  { label: "Bubble Threshold", model: bubbleThreshold, attrs: { min: 100, max: 255, type: "range" } },
  { label: "Min Circularity", model: minCircularity, attrs: { min: 0.01, max: 1.0, step: 0.01, type: "range" } },
  { label: "Bubble Min Area", model: bubbleMin, attrs: { min: 0.0001, max: 1.0, step: 0.0001, type: "range" } },
  { label: "Bubble Max Area", model: bubbleMax, attrs: { min: 0.0001, max: 1.0, step: 0.0001, type: "range" } }
];

function perfect_setup() {
  threshold.value = 100;
  blur.value = 5;
  morph.value = 5;
  minSize.value = 60;
  bubbleThreshold.value = 102;
  bubbleMin.value = 0.0028;
  bubbleMax.value = 0.1;
  minCircularity.value = 0.31;
}

async function applyDetection() {
  loading.value = true;
  error.value = null;
  try {
    const formData = new FormData();
    const imgResponse = await fetch(imageSrc.value);
    const blob = await imgResponse.blob();
    formData.append("file", blob, "upload.jpg");
    formData.append("blur", blur.value);
    formData.append("threshold", threshold.value);
    formData.append("morph", morph.value);
    formData.append("min_size", minSize.value);
    formData.append("bubble_thresh", bubbleThreshold.value);
    formData.append("bubble_min_area", bubbleMin.value);
    formData.append("bubble_max_area", bubbleMax.value);
    formData.append("min_circularity", minCircularity.value);

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
}
watch([blur, threshold, morph, minSize, bubbleThreshold, bubbleMin, bubbleMax, minCircularity],
  ([b, t, m, ms, bt, bmin, bmax, mc]) => {
    detectionParams.blur = b;
    detectionParams.threshold = t;
    detectionParams.morph = m;
    detectionParams.minSize = ms;
    detectionParams.bubbleThreshold = bt;
    detectionParams.bubbleMin = bmin;
    detectionParams.bubbleMax = bmax;
    detectionParams.minCircularity = mc;
  }
);
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
  justify-content: space-between; /* Even spacing */
  flex-wrap: nowrap; /* Prevent wrapping */
  gap: 4px; /* Smaller gap between buttons */
}

.tab-buttons button {
  flex: 1 1 auto; /* Buttons shrink and grow evenly */
  font-size: clamp(0.6rem, 1.5vw, 0.9rem); /* Small responsive text */
  padding: 0.3rem 0.4rem; /* Reduce padding */
  white-space: nowrap; /* Prevent text wrapping inside buttons */
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

/* Mobile layout: Image 33% height, Controls 66% */
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
