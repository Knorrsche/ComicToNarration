<template>
  <div class="content-wrapper">
    <div class="viewer-section" v-if="comic">
      <div class="controls">
        <button @click="prevPage" :disabled="pageIndex === 0">◀ Prev</button>
        <span>Page {{ pageIndex + 1 }} / {{ pages.length }}</span>
        <button @click="nextPage" :disabled="pageIndex === pages.length - 1">Next ▶</button>
      </div>

      <div v-if="imageSrc">
        <div class="buttons">
          <button :class="{ active: showPanels }" @click="showPanels = !showPanels" style="--active-color: #007bff">Panels</button>
          <button :class="{ active: showBubbles }" @click="showBubbles = !showBubbles" style="--active-color: #dc3545">Speech Bubbles</button>
          <button :class="{ active: showEntities }" @click="showEntities = !showEntities" style="--active-color: #28a745">Entities</button>
        </div>

        <div class="image-wrapper image-viewer" ref="wrapperRef">
          <img :src="imageSrc" @load="onImageLoad" ref="imageRef" alt="Processed comic" class="responsive-image" />
          <div
            v-for="(box, index) in filteredBoundingBoxes"
            :key="index"
            :class="['box-overlay', box.type]"
            :style="boxStyle(box)"
          >
            <span class="label">{{ box.type }}</span>
          </div>
        </div>
      </div>
    </div>

    <div class="scroller-section">
      <ComicScrollPanel />
    </div>
  </div>
</template>

<script setup>
import {computed, nextTick, onMounted, onUnmounted, ref, watch} from 'vue';
import {useRoute} from 'vue-router';
import ComicScrollPanel from "../components/ComicScrollPanel.vue";

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

    boundingBoxes.value = extractBoxesFromXml(xmlDoc, pageIndex.value+1);


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
  window.addEventListener("resize", updateScale);
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
.content-wrapper {
  display: flex;
  width: 100%;
  gap: 40px;
  justify-content: center;
  align-items: flex-start;
}

.viewer-section {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 20px;
  max-width: 65vw;
}

.controls {
  margin-bottom: 20px;
  display: flex;
  align-items: center;
  gap: 20px;
}

.image-viewer img {
  max-width: 100%;
  max-height: 80vh;
  border-radius: 8px;
  box-shadow: 0 0 12px rgba(0, 0, 0, 0.2);
}

.image-wrapper {
  position: relative;
  width: 100%;
  max-width: 600px;
  height: auto;
  aspect-ratio: auto;
}

.box-overlay {
  pointer-events: none;
  box-sizing: border-box;
  position: absolute;
}

.box-overlay.panel {
  border: 6px dashed blue;
}

.box-overlay.bubble {
  border: 6px solid red;
}

.box-overlay.entity {
  border: 6px dotted green;
}

.label {
  position: absolute;
  top: -1.2em;
  left: 0;
  background-color: rgba(0, 0, 0, 0.7);
  color: white;
  font-size: 0.7rem;
  padding: 2px 4px;
  border-radius: 3px;
  pointer-events: none;
  opacity: 0.7;
}

.buttons {
  margin-bottom: 15px;
  display: flex;
  justify-content: center;
  gap: 8px;
  flex-shrink: 0;
}

button {
  border: 1px solid #ccc;
  background-color: white;
  padding: 6px 14px;
  border-radius: 4px;
  cursor: pointer;
  user-select: none;
  font-weight: 600;
  transition: background-color 0.2s, border-color 0.2s;
}

button.active {
  background-color: var(--active-color);
  border-color: var(--active-color);
  color: white;
}
</style>
