<template>
  <div class="ml-page">
    <h1>Interactive Comic Panel & Speech Bubble Detection</h1>

    <div class="controls">
      <input type="file" accept="image/*" @change="handleImageUpload" />
      <div class="tab-buttons">
        <button @click="activeTab = 'panel'" :class="{ active: activeTab === 'panel' }">Panel Parameters</button>
        <button @click="activeTab = 'bubble'" :class="{ active: activeTab === 'bubble' }">Bubble Parameters</button>
      </div>
    </div>

    <div class="main-layout">
      <div class="image-panel">
        <img v-if="processedImageSrc" :src="processedImageSrc" alt="Processed Image" />
        <img v-else-if="imageSrc" :src="imageSrc" alt="Uploaded Image" />
      </div>
  <p>CHALLENGE: TRY TO FIND THE BEST DETECTION FOR YOU PAGE AND THEN LOOK HWO IT PERFORMS ON A DIFFERENT PAGE TO SEE HOW WELL IT GENERLIZES, NOTE: MAYBE ADD AN OPTION TO THEN TEST
  YOUR SETUP WITH OUR DATABASE AND GROUNT TRUTH TO SEE THE GENREALIZTION AND THE CHALLENGE OF THIS.
  NOTE2: USE COMIC, MANGA AND GRAPHIC NOVEL TO ALSO SHOW GENERALIZTION TO DIFFERENT STYLES</p>
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
            <label>Bubble Min Area: {{ bubbleMin }}</label>
            <input type="range" min="100" max="10000" v-model="bubbleMin" />
            <span title="Minimum size (area in pixels) of a bubble to detect.">ℹ️</span>
          </div>

          <div class="param-group">
            <label>Bubble Max Area: {{ bubbleMax }}</label>
            <input type="range" min="1000" max="30000" step="100" v-model="bubbleMax" />
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

const imageSrc = ref(null)
const processedImageSrc = ref(null)
const loading = ref(false)
const error = ref(null)

const blur = ref(5)
const threshold = ref(200)
const morph = ref(5)
const minSize = ref(50)
const bubbleThreshold = ref(220)
const bubbleMin = ref(1000)
const bubbleMax = ref(10000)

const activeTab = ref('panel')

function handleImageUpload(event) {
  const file = event.target.files[0]
  if (!file) return

  const reader = new FileReader()
  reader.onload = () => {
    imageSrc.value = reader.result
    processedImageSrc.value = null
    error.value = null
  }
  reader.readAsDataURL(file)
}

async function applyDetection() {
  if (!imageSrc.value) return

  loading.value = true
  error.value = null

  try {
    const formData = new FormData()
    const blob = dataURLtoBlob(imageSrc.value)
    formData.append('file', blob, 'upload.png')
    formData.append('blur', blur.value)
    formData.append('threshold', threshold.value)
    formData.append('morph', morph.value)
    formData.append('min_size', minSize.value)
    formData.append('bubble_thresh', bubbleThreshold.value)
    formData.append('bubble_min_area', bubbleMin.value)
    formData.append('bubble_max_area', bubbleMax.value)

    const response = await fetch('http://localhost:8000/api/process', {
      method: 'POST',
      body: formData,
    })

    if (!response.ok) throw new Error(`Server error: ${response.statusText}`)

    const blobResult = await response.blob()
    processedImageSrc.value = URL.createObjectURL(blobResult)
  } catch (err) {
    error.value = err.message || 'Image processing failed'
  } finally {
    loading.value = false
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

watch([blur, threshold, morph, minSize, bubbleThreshold, bubbleMin, bubbleMax], autoApply)
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

.main-layout {
  display: flex;
  gap: 30px;
  justify-content: center;
  align-items: flex-start;
  flex-wrap: wrap;
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