<template>
  <div class="layout">
    <!-- Hamburger Menu -->
    <button class="hamburger" @click="toggleMenu" aria-label="Toggle Menu">☰</button>

    <!-- Sidebar -->
    <nav class="sidebar" :class="{ open: isMenuOpen }">
      <ul>
        <li v-for="section in sections" :key="section.id">
          <a :href="'/#' + section.id" @click="isMenuOpen = false">{{ section.title }}</a>
        </li>
      </ul>
    </nav>

    <!-- Main Viewer Content -->
    <div class="content-wrapper">
      <div class="viewer-section" v-if="comic">
        <div v-if="imageSrc">
          <div class="buttons">
            <button :class="{ active: showPanels }" @click="showPanels = !showPanels" style="--active-color: #007bff">Panels</button>
            <button :class="{ active: showBubbles }" @click="showBubbles = !showBubbles" style="--active-color: #dc3545">Speech Bubbles</button>
            <button :class="{ active: showEntities }" @click="showEntities = !showEntities" style="--active-color: #28a745">Entities</button>
          </div>

          <!-- Image with Overlay Navigation -->
          <div class="image-wrapper image-viewer" ref="wrapperRef">
            <img :src="imageSrc" @load="onImageLoad" ref="imageRef" alt="Processed comic" class="responsive-image" />

            <!-- Overlay Nav Buttons -->
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

            <!-- Bounding Boxes without labels -->
            <div
              v-for="(box, index) in filteredBoundingBoxes"
              :key="index"
              :class="['box-overlay', box.type]"
              :style="boxStyle(box)"
            ></div>
          </div>
        </div>
      </div>

      <!-- Only show ComicScrollPanel if NOT on mobile -->
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

import HeaderPage from './HeaderPage.vue'
import InfoBoxPage from './InfoBoxPage.vue'
import GraphicNovelDifferencePage from './GraphicNovelDifferencePage.vue'
import ComicPartsPage from './ComicPartsPage.vue'
import ChallengesPage from './ChallengesPage.vue'
import InteractiveMlPage from './InteractiveMlPage.vue'
import InteractiveDlPage from './InteractiveDlPage.vue'

// Sidebar Menu Data
const sections = [
  { id: "header", title: "Intro", component: HeaderPage },
  { id: "info", title: "The Visual Impaired", component: InfoBoxPage },
  { id: "gn-diff", title: "Types of Graphic Novels", component: GraphicNovelDifferencePage },
  { id: "parts", title: "Parts of Comics", component: ComicPartsPage },
  { id: "challenges", title: "Challenges", component: ChallengesPage },
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

// Viewer Logic
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
  imageSrc.value = `http://localhost:8000/comics/${comic.value}/${currentPage}`;
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
  return {
    x: parts.x || 0,
    y: parts.y || 0,
    width: parts.width || 0,
    height: parts.height || 0,
  };
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

  imageWidth.value = img.clientWidth;
  imageHeight.value = img.clientHeight;

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
.layout {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
}

.hamburger {
  position: fixed;
  top: 1rem;
  left: 1rem;
  z-index: 1100;
  font-size: 1.5rem;
  background: rgba(218, 116, 52, 0.95);
  color: white;
  border: none;
  padding: 0.5rem 0.7rem;
  border-radius: 4px;
  cursor: pointer;
}

.sidebar {
  position: fixed;
  top: 0;
  left: -250px;
  height: 100vh;
  width: 250px;
  background-color: #da7434;
  padding-top: 2rem;
  z-index: 1000;
  transition: left 0.3s ease;
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
  margin: 1.5rem 0;
  text-align: center;
}
.sidebar a {
  color: white;
  text-decoration: none;
  font-weight: bold;
  transition: color 0.3s ease;
  display: block;
  padding: 0.5rem 0;
}
.sidebar a:hover,
.sidebar a.active {
  color: #00bfff;
}

.content-wrapper {
  display: flex;
  width: 100%;
  gap: 40px;
  justify-content: center;
  align-items: flex-start;
  flex-wrap: wrap;
}

.viewer-section {
  display: flex;
  flex-direction: column;
  align-items: center;
  max-width: 65vw;
}

.scroller-section {
  width: 100%;
}

.image-wrapper {
  position: relative;
  width: 100%;
  max-width: 600px;
}

.image-viewer img {
  max-width: 100%;
  max-height: 80vh;
  border-radius: 8px;
  box-shadow: 0 0 12px rgba(0, 0, 0, 0.2);
}

/* Overlay Nav Buttons */
.image-nav-btn {
  position: absolute;
  top: 50%;
  transform: translateY(-50%);
  background: rgba(0, 0, 0, 0.4);
  color: white;
  font-size: 2rem;
  padding: 0.5rem 0.8rem;
  border: none;
  border-radius: 50%;
  cursor: pointer;
}
.image-nav-btn.left {
  left: 10px;
}
.image-nav-btn.right {
  right: 10px;
}
.image-nav-btn:hover {
  background: rgba(0, 0, 0, 0.6);
}
.image-nav-btn:disabled {
  background: rgba(0, 0, 0, 0.2);
}

/* Bounding Boxes */
.box-overlay {
  pointer-events: none;
  position: absolute;
}
.box-overlay.panel {
  border: 3px dashed blue;
}
.box-overlay.bubble {
  border: 3px solid red;
}
.box-overlay.entity {
  border: 3px dotted green;
}

/* Buttons Row */
.buttons {
  margin-bottom: 15px;
  display: flex;
  justify-content: center;
  gap: 8px;
}

button.active {
  background-color: var(--active-color);
  color: white;
}

/* Mobile Layout */
@media (max-width: 768px) {
  .content-wrapper {
    flex-direction: column;
    gap: 20px;
  }

  .viewer-section {
    max-width: 100%;
  }

  .image-viewer img {
    max-height: 60vh;
  }
}
</style>
