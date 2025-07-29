<template>
  <div class="ml-page">
    <h1>Interactive Comic Panel & Speech Bubble Detection</h1>

    <div class="controls">
      <div class="tab-buttons">
        <button @click="activeTab = 'panel'" :class="{ active: activeTab === 'panel' }">Panel Parameters</button>
        <button @click="activeTab = 'bubble'" :class="{ active: activeTab === 'bubble' }">Bubble Parameters</button>
      <button @click="perfect_setup">Perfect Setup</button>
      </div>
    </div>

    <div class="content-wrapper">
      <div class="explanation-box">
        <h3>Machine Learning in Comics</h3>
        <p>
          Deep learning is a subset of machine learning that uses layered neural networks (like CNNs or transformers) to automatically learn features from large datasets. Unlike traditional machine learning, which requires handcrafted features (e.g. edge detectors or geometric rules), deep learning models learn directly from raw pixel data — enabling them to identify complex patterns in comic images.
        </p>
        <p>
          In the context of comics, deep learning allows automatic detection and interpretation of panels, speech bubbles, characters, and even emotions or narrative structure. This mimics how humans visually understand and follow stories, enabling smarter comic viewers and tools.
        </p>
      </div>
          <div class="image-panel">
        <img v-if="processedImageSrc" :src="processedImageSrc" alt="Processed Image" />
        <img v-else-if="imageSrc" :src="imageSrc" alt="Uploaded Image" />
      </div>

      <div class="interaction-panel" v-if="imageSrc">
        <h3>Detection Parameters</h3>

        <template v-if="activeTab === 'panel'">
          <div class="param-group">
            <label>Blur Kernel Size: {{ blur }}</label>
            <input type="range" min="1" max="15" step="2" v-model="blur" />
            <span title="Applies blur to reduce noise. Higher values make panel edges softer.">ℹ️</span>
          </div>

          <div class="param-group">
            <label>Threshold: {{ threshold }}</label>
            <input type="range" min="0" max="255" v-model="threshold" />
            <span title="Threshold for detecting dark lines. Lower = more sensitive.">ℹ️</span>
          </div>

          <div class="param-group">
            <label>Morph Kernel Size: {{ morph }}</label>
            <input type="range" min="1" max="15" step="2" v-model="morph" />
            <span title="Fills small gaps in panel borders. Higher values fill more aggressively.">ℹ️</span>
          </div>

          <div class="param-group">
            <label>Min Panel Size: {{ minSize }}</label>
            <input type="range" min="10" max="300" v-model="minSize" />
            <span title="Minimum width/height for a region to be counted as a panel.">ℹ️</span>
          </div>
        </template>

        <template v-else>
          <div class="param-group">
            <label>Bubble Threshold: {{ bubbleThreshold }}</label>
            <input type="range" min="100" max="255" v-model="bubbleThreshold" />
            <span title="Pixel intensity threshold to find bright speech bubbles.">ℹ️</span>
          </div>

                  <div class="param-group">
            <label>Min Circularity: {{ minCircularity }}</label>
            <input type="range" min="0.01" max="1.0" step="0.01" v-model="minCircularity" />
            <span title="Minimum degree of circularity of detected patches.">ℹ️</span>
          </div>

          <div class="param-group">
            <label>Bubble Min Area: {{ bubbleMin }}</label>
            <input type="range" min="0.0001" max="1.0"  step="0.0001" v-model="bubbleMin" />
            <span title="Minimum size (area in pixels) of a bubble to detect.">ℹ️</span>
          </div>

          <div class="param-group">
            <label>Bubble Max Area: {{ bubbleMax }}</label>
            <input type="range" min="0.0001" max="1.0" step="0.0001" v-model="bubbleMax" />
            <span title="Maximum size (area in pixels) of a bubble to detect.">ℹ️</span>
          </div>
        </template>

        <button :disabled="!imageSrc || loading" @click="applyDetection">Apply Detection</button>
        <button :disabled="!imageSrc" @click="resetImage">Reset</button>
      </div>

      <div v-if="loading" class="loading">Processing image, please wait...</div>
      <div v-if="error" class="error">{{ error }}</div>
    </div>
  </div>
</template>

<script setup>
import {ref, watch} from 'vue'
import debounce from 'lodash/debounce'
import ComicImage from "../assets/Normal.jpg"

const imageSrc = ref(ComicImage)
const processedImageSrc = ref(null)
const loading = ref(false)
const error = ref(null)

const blur = ref(5)
const threshold = ref(100)
const morph = ref(5)
const minSize = ref(10)
const bubbleThreshold = ref(150)
const bubbleMin = ref(0.0001)
const bubbleMax = ref(0.1)
const minCircularity = ref(0.4)

const activeTab = ref('panel')

function perfect_setup() {
    threshold.value = 100
    blur.value = 5
    morph.value = 5
    minSize.value = 60
    bubbleThreshold.value = 102
    bubbleMin.value = 0.0028
    bubbleMax.value = 0.1
    minCircularity.value = 0.31
}

async function applyDetection() {
  if (!imageSrc.value) return;

  loading.value = true;
  error.value = null;

  try {
    const formData = new FormData();

    const imgResponse = await fetch(imageSrc.value);
    const blob = await imgResponse.blob();

    formData.append('file', blob, 'upload.jpg');
    formData.append('blur', blur.value);
    formData.append('threshold', threshold.value);
    formData.append('morph', morph.value);
    formData.append('min_size', minSize.value);
    formData.append('bubble_thresh', bubbleThreshold.value);
    formData.append('bubble_min_area', bubbleMin.value);
    formData.append('bubble_max_area', bubbleMax.value);
    formData.append('min_circularity',minCircularity.value)

    const serverRes = await fetch('http://localhost:8000/api/process', {
      method: 'POST',
      body: formData,
    });

    if (!serverRes.ok) throw new Error(`Server error: ${serverRes.statusText}`);

    const blobResult = await serverRes.blob();
    processedImageSrc.value = URL.createObjectURL(blobResult);
  } catch (err) {
    error.value = err.message || 'Image processing failed';
  } finally {
    loading.value = false;
  }
}


function resetImage() {
  processedImageSrc.value = null
  error.value = null
}

function dataURLtoBlob(dataurl) {
  const arr = dataurl.split(',')
  const mime = arr[0].match(/:(.*?);/)[1]
  const bstr = atob(arr[1])
  let n = bstr.length
  const u8arr = new Uint8Array(n)
  while (n--) {
    u8arr[n] = bstr.charCodeAt(n)
  }
  return new Blob([u8arr], {type: mime})
}

const autoApply = debounce(() => {
  if (imageSrc.value) applyDetection()
}, 500)

watch([blur, threshold, morph, minSize, bubbleThreshold, bubbleMin, bubbleMax,minCircularity], autoApply)
</script>

<style scoped>
.ml-page {
  padding: 20px;
  font-family: sans-serif;
  text-align: center;
}

.controls {
  margin-bottom: 20px;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 12px;
}

.tab-buttons button {
  margin: 0 6px;
  padding: 6px 12px;
  border: none;
  cursor: pointer;
  background: #e0e0e0;
  border-radius: 4px;
}

.tab-buttons button.active {
  background-color: #007bff;
  color: white;
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
  padding: 15px;
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

.image-panel img {
  max-width: 400px;
  border-radius: 8px;
  border: 1px solid #ccc;
}

.interaction-panel {
  width: 420px;
  text-align: left;
  background: #f7f7f7;
  padding: 16px;
  border-radius: 8px;
}

.param-group {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 12px;
}

.loading {
  margin-top: 20px;
  font-weight: bold;
  color: #007bff;
}

.error {
  margin-top: 20px;
  color: #d9534f;
  font-weight: bold;
}
</style>