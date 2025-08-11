<template>
<div :class="['layout', { exiting: isExiting }]">
  <button class="return-btn" @click="goBack" aria-label="Go Back">
  <svg
    xmlns="http://www.w3.org/2000/svg"
    width="64"
    height="64"
    viewBox="0 0 45.58 45.58"
    fill="var(--orange)"
  >
    <path
      d="M45.506,33.532c-1.741-7.42-7.161-17.758-23.554-19.942V7.047c0-1.364-0.826-2.593-2.087-3.113
      c-1.261-0.521-2.712-0.229-3.675,0.737L1.305,19.63c-1.739,1.748-1.74,4.572-0.001,6.32L16.19,40.909
      c0.961,0.966,2.415,1.258,3.676,0.737c1.261-0.521,2.087-1.75,2.087-3.113v-6.331c5.593,0.007,13.656,0.743,19.392,4.313
      c0.953,0.594,2.168,0.555,3.08-0.101C45.335,35.762,45.763,34.624,45.506,33.532z"
    />
  </svg>
</button>

    <div class="content-wrapper">
      <div class="viewer-section" v-if="comic">
        <div v-if="imageSrc" class="viewer-card">
          <div class="buttons">
            <button :class="{ active: showPanels }" @click="showPanels = !showPanels" style="--active-color: #007bff">
              Panels
            </button>
            <button :class="{ active: showBubbles }" @click="showBubbles = !showBubbles" style="--active-color: #dc3545">
              Speech Bubbles
            </button>
            <button :class="{ active: showEntities }" @click="showEntities = !showEntities" style="--active-color: #28a745">
              Entities
            </button>
            <button :disabled="loading" @click="applyDetection" style="--active-color: #ff9800">
              {{ loading ? 'Processing...' : detectionActive ? 'Remove Detection' : 'Apply Manual Detection' }}
            </button>
          </div>

          <div class="image-viewer" ref="wrapperRef">
            <img
              :src="imageSrc"
              @load="onImageLoad"
              ref="imageRef"
              alt="Processed comic"
              class="comic-image"
            />

<button
  class="image-nav-btn left"
  @click="prevPage"
  :disabled="pageIndex === 0"
  aria-label="Previous Page"
>
  <svg
    fill="var(--orange)"
    viewBox="0 0 45.513 45.512"
    width="36"
    height="36"
    xmlns="http://www.w3.org/2000/svg"
    transform="rotate(180)"
  >
    <path
      d="M44.275,19.739L30.211,5.675c-0.909-0.909-2.275-1.18-3.463-0.687c-1.188,0.493-1.959,1.654-1.956,2.938l0.015,5.903
      l-21.64,0.054C1.414,13.887-0.004,15.312,0,17.065l0.028,11.522c0.002,0.842,0.338,1.648,0.935,2.242
      s1.405,0.927,2.247,0.925l21.64-0.054l0.014,5.899c0.004,1.286,0.781,2.442,1.971,2.931c1.189,0.487,2.557,0.21,3.46-0.703
      L44.29,25.694C45.926,24.043,45.92,21.381,44.275,19.739z"
    />
  </svg>
</button>

<button
  class="image-nav-btn right"
  @click="nextPage"
  :disabled="pageIndex === pages.length - 1"
  aria-label="Next Page"
>
  <svg
    fill="var(--orange)"
    viewBox="0 0 45.513 45.512"
    width="36"
    height="36"
    xmlns="http://www.w3.org/2000/svg"
  >
    <path
      d="M44.275,19.739L30.211,5.675c-0.909-0.909-2.275-1.18-3.463-0.687c-1.188,0.493-1.959,1.654-1.956,2.938l0.015,5.903
      l-21.64,0.054C1.414,13.887-0.004,15.312,0,17.065l0.028,11.522c0.002,0.842,0.338,1.648,0.935,2.242
      s1.405,0.927,2.247,0.925l21.64-0.054l0.014,5.899c0.004,1.286,0.781,2.442,1.971,2.931c1.189,0.487,2.557,0.21,3.46-0.703
      L44.29,25.694C45.926,24.043,45.92,21.381,44.275,19.739z"
    />
  </svg>
</button>


            <div
              v-for="(box, index) in filteredBoundingBoxes"
              :key="index"
              :class="['box-overlay', box.type]"
              :style="boxStyle(box)"
            ></div>
          </div>
        </div>
      </div>

      <div class="scroller-section" v-if="!isMobile">
        <ComicScrollPanel />
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, nextTick, onMounted, onUnmounted, ref, watch } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import ComicScrollPanel from "../components/ComicScrollPanel.vue";
import { detectionParams } from "../stores/detectionParams";

const router = useRouter();
const isExiting = ref(false);

const goBack = () => {
  isExiting.value = true;
  setTimeout(() => {
    router.push({ path: '/' });
  }, 300);
};

const isMobile = ref(false);
const checkMobile = () => {
  isMobile.value = window.innerWidth <= 768;
};

const route = useRoute();
const comic = ref(route.params.comic);
const pages = ref([]);
const pageIndex = ref(0);
const imageSrc = ref('');
const imageRef = ref(null);
const wrapperRef = ref(null);
const boundingBoxes = ref([]);

const showPanels = ref(true);
const showBubbles = ref(true);
const showEntities = ref(true);

const scaleX = ref(1);
const scaleY = ref(1);
const offsetX = ref(0);
const offsetY = ref(0);

const loading = ref(false);
const detectionActive = ref(false);
const processedImageSrc = ref(null);
const originalImageSrc = ref('');

async function applyDetection() {
  if (!imageSrc.value) return;

  if (detectionActive.value) {
    imageSrc.value = originalImageSrc.value;
    detectionActive.value = false;
    return;
  }

  loading.value = true;
  try {
    const formData = new FormData();
    formData.append("comic", comic.value);
    formData.append("page", pages.value[pageIndex.value]);
    formData.append("blur", detectionParams.blur);
    formData.append("threshold", detectionParams.threshold);
    formData.append("morph", detectionParams.morph);
    formData.append("min_size", detectionParams.minSize);
    formData.append("bubble_thresh", detectionParams.bubbleThreshold);
    formData.append("bubble_min_area", detectionParams.bubbleMin);
    formData.append("bubble_max_area", detectionParams.bubbleMax);
    formData.append("min_circularity", detectionParams.minCircularity);

    const res = await fetch("http://localhost:8000/api/process", {
      method: "POST",
      body: formData
    });

    if (!res.ok) throw new Error(`Server error: ${res.statusText}`);

    const blobResult = await res.blob();
    processedImageSrc.value = URL.createObjectURL(blobResult);
    imageSrc.value = processedImageSrc.value;
    detectionActive.value = true;
  } catch (err) {
    console.error("Detection failed:", err);
  } finally {
    loading.value = false;
  }
}

const fetchPages = async () => {
  const res = await fetch('http://localhost:8000/comics');
  const data = await res.json();
  const selected = data.find(c => c.name === comic.value);
  if (selected) {
    pages.value = selected.pages;
    loadImage();
  }
};

const loadImage = async () => {
  const currentPage = pages.value[pageIndex.value];
  originalImageSrc.value = `http://localhost:8000/comics/${comic.value}/${currentPage}`;
  imageSrc.value = originalImageSrc.value;
  detectionActive.value = false;
  await fetchAnnotationXml();
};

const fetchAnnotationXml = async () => {
  try {
    const res = await fetch(`http://localhost:8000/comics/${comic.value}.xml`);
    const text = await res.text();

    const parser = new DOMParser();
    const xmlDoc = parser.parseFromString(text, "application/xml");
    boundingBoxes.value = extractBoxesFromXml(xmlDoc, pageIndex.value + 1);

    await nextTick();
    updateScale();
  } catch (error) {
    console.error("Failed to load annotation XML:", error);
  }
};

const nextPage = () => {
  if (pageIndex.value < pages.value.length - 1) {
    pageIndex.value++;
    loadImage();
  }
};

const prevPage = () => {
  if (pageIndex.value > 0) {
    pageIndex.value--;
    loadImage();
  }
};

onMounted(() => {
  fetchPages();
  checkMobile();
  window.addEventListener("resize", () => {
    updateScale();
    checkMobile();
  });
});

onUnmounted(() => {
  window.removeEventListener("resize", updateScale);
});

watch(() => route.params.comic, (newVal) => {
  comic.value = newVal;
  pageIndex.value = 0;
  fetchPages();
});

const filteredBoundingBoxes = computed(() =>
  boundingBoxes.value.filter((box) => {
    if (box.type === "panel" && !showPanels.value) return false;
    if (box.type === "bubble" && !showBubbles.value) return false;
    if (box.type === "entity" && !showEntities.value) return false;
    return true;
  })
);

const parseBoundingBox = (bboxString) => {
  const parts = bboxString.split(",").reduce((acc, part) => {
    const [key, value] = part.split(":").map((s) => s.trim());
    acc[key] = parseFloat(value);
    return acc;
  }, {});
  return { x: parts.x || 0, y: parts.y || 0, width: parts.width || 0, height: parts.height || 0 };
};

const extractBoxesFromXml = (xmlDoc, currentPageIndex) => {
  const boxes = [];
  const pageNodes = xmlDoc.getElementsByTagName("Page");
  for (const pageNode of pageNodes) {
    const indexNode = pageNode.getElementsByTagName("Index")[0];
    if (!indexNode) continue;
    const index = parseInt(indexNode.textContent);
    if (index !== currentPageIndex) continue;

    const collect = (tag, type) => {
      const nodes = pageNode.getElementsByTagName(tag);
      for (const node of nodes) {
        const bboxNode = node.getElementsByTagName("BoundingBox")[0];
        if (bboxNode) {
          const bbox = parseBoundingBox(bboxNode.textContent);
          boxes.push({ ...bbox, type });
        }
      }
    };

    collect("Panel", "panel");
    collect("SpeechBubble", "bubble");
    collect("Entity", "entity");
  }
  return boxes;
};

const updateScale = () => {
  const img = imageRef.value;
  const container = wrapperRef.value;
  if (!img || img.naturalWidth === 0 || !container) return;

  const imgRect = img.getBoundingClientRect();
  const containerRect = container.getBoundingClientRect();

  scaleX.value = imgRect.width / img.naturalWidth;
  scaleY.value = imgRect.height / img.naturalHeight;

  offsetX.value = imgRect.left - containerRect.left;
  offsetY.value = imgRect.top - containerRect.top;
};

const onImageLoad = async () => {
  await nextTick();
  updateScale();
};

const boxStyle = (box) => ({
  top: `${box.y * scaleY.value + offsetY.value}px`,
  left: `${box.x * scaleX.value + offsetX.value}px`,
  width: `${box.width * scaleX.value}px`,
  height: `${box.height * scaleY.value}px`,
  position: "absolute",
});
</script>

<style scoped>
:global(:root) {
  --orange: #da7434;
  --orange-hover: #c45d1f;
}

.layout {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
  transition: opacity 0.3s ease;
  opacity: 1;
}
.layout.exiting {
  opacity: 0;
  pointer-events: none;
}
.return-btn {
  position: fixed;
  top: 1rem;
  left: 1rem;
  z-index: 1100;
  background: none;
  border: none;
  padding: 0;
  cursor: pointer;
  transition: transform 0.2s ease;
}
.return-btn:hover svg {
  fill: var(--orange-hover);
  transform: scale(1.1);
}

.content-wrapper {
  display: flex;
  width: 100%;
  gap: 2rem;
  justify-content: center;
  align-items: flex-start;
  flex-wrap: wrap;
  padding: 2rem;
}

.viewer-section {
  display: flex;
  flex-direction: column;
  align-items: center;
  max-width: 65vw;
}

.viewer-card {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  padding: 1.5rem;
  background: rgba(255, 255, 255, 0.8);
  backdrop-filter: blur(12px);
  border-radius: 16px;
  box-shadow: 0 4px 25px rgba(0, 0, 0, 0.08);
  align-items: center;
}

.image-viewer {
  position: relative;
  width: 100%;
  max-width: 600px;
  background: rgba(255, 255, 255, 0.75);
  backdrop-filter: blur(12px);
  border-radius: 16px;
  box-shadow: 0 4px 20px rgba(0,0,0,0.08);
  overflow: hidden;
}

.comic-image {
  width: 100%;
  height: auto;
  object-fit: contain;
  max-height: 80vh;
  border-radius: 12px;
}

.image-nav-btn {
  position: absolute;
  top: 50%;
  transform: translateY(-50%) scale(1.05);
  background: transparent;
  color: var(--orange);
  font-size: clamp(1.5rem, 3vw, 2rem);
  padding: 0.6rem;
  border-radius: 50px;
  cursor: pointer;
  transition: all 0.25s ease;
  box-shadow: none;
  z-index: 10;
  display: flex;
  align-items: center;
  justify-content: center;

  border: 2px solid var(--orange);
}

.image-nav-btn:hover:not(:disabled) {
  border-color: var(--orange-light);
  transform: translateY(-50%) scale(1.3);
  box-shadow: 0 4px 12px rgba(218, 116, 52, 0.3);
}

.image-nav-btn:active:not(:disabled) {
  transform: translateY(-50%) scale(1.05);
}

.image-nav-btn:disabled {
  color: rgba(0, 0, 0, 0.1);
  background: rgba(0, 0, 0, 0.05);
  transform: translateY(-50%) scale(1);
  cursor: default;
  border: 2px solid gray;
}

.image-nav-btn:disabled svg {
  fill: gray;
}
.image-nav-btn.left { left: 1rem; }
.image-nav-btn.right { right: 1rem; }


.box-overlay {
  pointer-events: none;
  position: absolute;
  border-radius: 4px;
}
.box-overlay.panel {
  border: 3px solid rgba(0, 123, 255, 0.7);
  box-shadow: 0 0 6px rgba(0, 123, 255, 0.6);
}
.box-overlay.bubble {
  border: 3px solid rgba(220, 53, 69, 0.7);
  box-shadow: 0 0 6px rgba(220, 53, 69, 0.6);
}
.box-overlay.entity {
  border: 3px solid rgba(40, 167, 69, 0.7);
  box-shadow: 0 0 6px rgba(40, 167, 69, 0.6);
}

.buttons {
  margin-bottom: 15px;
  display: flex;
  justify-content: center;
  gap: 8px;
  flex-wrap: wrap;
}
.buttons button {
  padding: 0.5rem 0.8rem;
  border: none;
  border-radius: 20px;
  background: #f0f0f0;
  cursor: pointer;
  font-weight: 500;
  transition: all 0.2s ease;
}
.buttons button:hover {
  background: #e2e2e2;
}
button.active {
  background-color: var(--active-color);
  color: white;
}

@media (max-width: 768px) {
  .image-nav-btn {
    background: transparent !important;
    box-shadow: none !important;
    color: var(--orange);
    padding: 0.4rem;
  }
  .image-nav-btn.left { left: 0.5rem; }
  .image-nav-btn.right { right: 0.5rem; }
  .content-wrapper {
    flex-direction: column;
    gap: 20px;
    padding: 1rem;
  }
  .viewer-section {
    max-width: 100%;
  }
  .comic-image {
    max-height: 60vh;
  }
}
</style>
