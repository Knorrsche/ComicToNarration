<template>
  <div class="layout">
    <!-- Modern Hamburger Menu -->
    <button class="hamburger" @click="toggleMenu" aria-label="Toggle Menu">
      <span></span>
      <span></span>
      <span></span>
    </button>

    <!-- Sidebar -->
    <nav class="sidebar" :class="{ open: isMenuOpen }">
      <ul>
        <li v-for="section in sections" :key="section.id">
          <a :href="'/#' + section.id" @click="isMenuOpen = false">{{ section.title }}</a>
        </li>
      </ul>
    </nav>

    <!-- Main Content -->
    <div class="content-wrapper">
      <!-- Viewer Section -->
      <div class="viewer-section" v-if="comic">
        <div v-if="imageSrc">
          <!-- Controls -->
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
              {{ loading ? 'Processing...' : detectionActive ? 'Remove Detection' : 'Apply Detection' }}
            </button>
          </div>

          <!-- Image Viewer -->
          <div class="image-viewer" ref="wrapperRef">
            <img :src="imageSrc" @load="onImageLoad" ref="imageRef" alt="Processed comic" class="comic-image" />

            <!-- Navigation Buttons -->
            <button
              class="image-nav-btn left"
              @click="prevPage"
              :disabled="pageIndex === 0"
              aria-label="Previous Page"
            >
              ◀
            </button>
            <button
              class="image-nav-btn right"
              @click="nextPage"
              :disabled="pageIndex === pages.length - 1"
              aria-label="Next Page"
            >
              ▶
            </button>

            <!-- Bounding Boxes -->
            <div
              v-for="(box, index) in filteredBoundingBoxes"
              :key="index"
              :class="['box-overlay', box.type]"
              :style="boxStyle(box)"
            ></div>
          </div>
        </div>
      </div>

      <!-- Comic List (hidden on mobile) -->
      <div class="scroller-section" v-if="!isMobile">
        <ComicScrollPanel />
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, nextTick, onMounted, onUnmounted, ref, watch } from 'vue';
import { useRoute } from 'vue-router';
import ComicScrollPanel from "../components/ComicScrollPanel.vue";
import { detectionParams } from "../stores/detectionParams";

import Header from '../components/Header.vue'
import InfoBox from '../components/InfoBox.vue'
import GraphicNovelDifference from '../components/GraphicNovelDifference.vue'
import ComicParts from '../components/ComicParts.vue'
import Challenges from '../components/Challenges.vue'
import InteractiveMlPage from './InteractiveMlPage.vue'
import InteractiveDlPage from './InteractiveDlPage.vue'

// Sidebar Menu
const sections = [
  { id: "header", title: "Intro", component: Header },
  { id: "info", title: "The Visual Impaired", component: InfoBox },
  { id: "gn-diff", title: "Types of Graphic Novels", component: GraphicNovelDifference },
  { id: "parts", title: "Parts of Comics", component: ComicParts },
  { id: "challenges", title: "Challenges", component: Challenges },
  { id: "ml", title: "Machine Learning", component: InteractiveMlPage },
  { id: "dl", title: "Deep Learning", component: InteractiveDlPage }
]

const isMenuOpen = ref(false);
const toggleMenu = () => {
  isMenuOpen.value = !isMenuOpen.value;
};

// Mobile detection
const isMobile = ref(false);
const checkMobile = () => {
  isMobile.value = window.innerWidth <= 768;
};

// Viewer logic
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

const imageWidth = ref(0);
const imageHeight = ref(0);
const scaleX = ref(1);
const scaleY = ref(1);

const loading = ref(false);
const detectionActive = ref(false);
const processedImageSrc = ref(null);
const originalImageSrc = ref('');

// Apply detection
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

// Fetch pages
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

// Filter boxes
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
  if (!img || img.naturalWidth === 0) return;

  const rect = img.getBoundingClientRect();
  const containerRect = wrapperRef.value.getBoundingClientRect();

  // Scale based on actual rendered image dimensions
  imageWidth.value = rect.width;
  imageHeight.value = rect.height;

  scaleX.value = imageWidth.value / img.naturalWidth;
  scaleY.value = imageHeight.value / img.naturalHeight;
};

const onImageLoad = () => {
  updateScale();
};

const boxStyle = (box) => ({
  top: `${box.y * scaleY.value}px`,
  left: `${box.x * scaleX.value}px`,
  width: `${box.width * scaleX.value}px`,
  height: `${box.height * scaleY.value}px`,
  position: "absolute",
});
</script>

<style scoped>
:root {
  --orange: #da7434;
  --orange-hover: #c45d1f;
}

/* Layout */
.layout {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
}

/* Modern Hamburger */
.hamburger {
  position: fixed;
  top: 1rem;
  left: 1rem;
  z-index: 1100;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  width: 34px;
  height: 26px;
  background: white;
  border: 2px solid var(--orange);
  border-radius: 8px;
  padding: 6px;
  cursor: pointer;
  transition: background 0.3s ease, transform 0.2s ease;
}
.hamburger:hover {
  background: #fff4ee;
  transform: scale(1.05);
}
.hamburger span {
  display: block;
  height: 3px;
  background: var(--orange);
  border-radius: 2px;
}

/* Sidebar with glass effect */
.sidebar {
  position: fixed;
  top: 0;
  left: -250px;
  height: 100vh;
  width: 250px;
  background: rgba(255, 255, 255, 0.85);
  backdrop-filter: blur(12px);
  padding-top: 4rem;
  z-index: 1000;
  transition: left 0.3s ease;
  box-shadow: 2px 0 8px rgba(0,0,0,0.15);
}
.sidebar.open {
  left: 0;
}
.sidebar ul {
  list-style: none;
  padding: 0;
  margin: 0;
}
.sidebar li {
  margin: 1.2rem 0;
  text-align: center;
}
.sidebar a {
  color: var(--orange);
  text-decoration: none;
  font-weight: 600;
  transition: color 0.3s ease;
}
.sidebar a:hover {
  color: var(--orange-hover);
}

/* Content layout */
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

/* Glass style image viewer */
.image-viewer {
  position: relative;
  width: 100%;
  max-width: 600px;
  background: rgba(255, 255, 255, 0.75);
  backdrop-filter: blur(12px);
  border-radius: 16px;
  box-shadow: 0 4px 20px rgba(0,0,0,0.08);
  overflow: hidden; /* ensures overlays align */
}

.comic-image {
  max-width: 100%;
  max-height: 80vh;
  border-radius: 12px;
}

/* Overlay Nav Buttons */
.image-nav-btn {
  position: absolute;
  top: 50%;
  transform: translateY(-50%);
  background: var(--orange);
  color: white;
  font-size: 1.8rem;
  padding: 0.5rem 0.8rem;
  border: none;
  border-radius: 50%;
  cursor: pointer;
  box-shadow: 0 3px 6px rgba(0,0,0,0.15);
  transition: all 0.2s ease;
}
.image-nav-btn:hover {
  background: var(--orange-hover);
  transform: translateY(-50%) scale(1.05);
}
.image-nav-btn:disabled {
  background: rgba(0,0,0,0.2);
  cursor: default;
}
.image-nav-btn.left {
  left: 10px;
}
.image-nav-btn.right {
  right: 10px;
}

/* Bounding boxes with glow */
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

/* Control buttons */
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

/* Mobile layout */
@media (max-width: 768px) {
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
