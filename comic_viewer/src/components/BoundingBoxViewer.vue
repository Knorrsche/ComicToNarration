<template>
  <div class="outer-container">
    <div class="buttons">
      <button
          :class="{ active: showPanels }"
          @click="showPanels = !showPanels"
          style="--active-color: #007bff"

      >
        Panels
      </button>
      <button
          :class="{ active: showBubbles }"
          @click="showBubbles = !showBubbles"
          style="--active-color: #dc3545"

      >
        Speech Bubbles
      </button>
      <button
          :class="{ active: showEntities }"
          @click="showEntities = !showEntities"
          style="--active-color: #28a745"

      >
        Entities
      </button>
    </div>

    <div class="image-wrapper" ref="wrapperRef">
      <img
          :src="imageSrc"
          @load="onImageLoad"
          ref="imageRef"
          alt="Loaded from API"
      />
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
</template>


<script setup>
import {ref, onMounted, watch, computed} from 'vue';

const imageSrc = ref('');
const imageRef = ref(null);
const wrapperRef = ref(null);
const currentIndex = ref(1);
const boundingBoxes = ref([]);
const boxesByPageIndex = ref({});
const scaleX = ref(1);
const scaleY = ref(1);

const showPanels = ref(true);
const showBubbles = ref(true);
const showEntities = ref(true);

const filteredBoundingBoxes = computed(() =>
    boundingBoxes.value.filter((box) => {
      if (box.type === 'panel' && !showPanels.value) return false;
      if (box.type === 'bubble' && !showBubbles.value) return false;
      if (box.type === 'entity' && !showEntities.value) return false;
      return true;
    })
);

const parseBoundingBox = (bboxString) => {
  const parts = bboxString.split(',').reduce((acc, part) => {
    const [key, value] = part.split(':').map(s => s.trim());
    acc[key] = parseFloat(value);
    return acc;
  }, {});
  return {
    x: parts.x,
    y: parts.y,
    width: parts.width,
    height: parts.height,
  };
};

const extractBoxesFromPage = (page) => {
  const boxes = [];
  const collect = (tag, type) => {
    const nodes = page.getElementsByTagName(tag);
    for (const node of nodes) {
      const bboxNode = node.getElementsByTagName('BoundingBox')[0];
      if (bboxNode) {
        const bbox = parseBoundingBox(bboxNode.textContent);
        boxes.push({...bbox, type});
      }
    }
  };
  collect('Panel', 'panel');
  collect('SpeechBubble', 'bubble');
  collect('Entity', 'entity');
  return boxes;
};

const updateBoundingBoxesForPage = () => {
  boundingBoxes.value = boxesByPageIndex.value[currentIndex.value] || [];
};

const fetchXmlData = async (xmlUrl) => {
  try {
    const response = await fetch(xmlUrl);
    const xmlText = await response.text();
    const parser = new DOMParser();
    const xmlDoc = parser.parseFromString(xmlText, 'application/xml');

    const pageSides = ['LeftPage', 'RightPage'];
    const pagePairs = xmlDoc.getElementsByTagName('PagePair');
    for (const pair of pagePairs) {
      for (const side of pageSides) {
        const pageWrapper = pair.getElementsByTagName(side)[0];
        if (!pageWrapper) continue;

        const page = pageWrapper.getElementsByTagName('Page')[0];
        if (!page) continue;

        const indexNode = page.getElementsByTagName('Index')[0];
        if (!indexNode) continue;

        const pageIndex = parseInt(indexNode.textContent);
        boxesByPageIndex.value[pageIndex] = extractBoxesFromPage(page);
      }
    }
    updateBoundingBoxesForPage();
  } catch (error) {
    console.error('Failed to parse XML:', error);
  }
};

const fetchImageAndBoxes = async () => {
  try {
    const response = await fetch('http://localhost:8000/get-comic');
    if (!response.ok) throw new Error('Failed to fetch comic data');

    const data = await response.json();
    imageSrc.value = 'http://localhost:8000' + data.image_url;
    await fetchXmlData('http://localhost:8000' + data.xml_url);
  } catch (error) {
    console.error('Error loading comic data:', error);
  }
};

const boxStyle = (box) => ({
  top: `${box.y * scaleY.value}px`,
  left: `${box.x * scaleX.value}px`,
  width: `${box.width * scaleX.value}px`,
  height: `${box.height * scaleY.value}px`,
  position: 'absolute',
});

const onImageLoad = () => {
  const img = imageRef.value;
  if (!img) return;

  const naturalWidth = img.naturalWidth;
  const naturalHeight = img.naturalHeight;
  const renderedWidth = img.clientWidth;
  const renderedHeight = img.clientHeight;

  scaleX.value = renderedWidth / naturalWidth;
  scaleY.value = renderedHeight / naturalHeight;
};

onMounted(() => {
  fetchImageAndBoxes();
});

watch(currentIndex, updateBoundingBoxesForPage);
</script>

<style scoped>
.outer-container {
  text-align: center;
  margin-top: 20px;
}

.image-wrapper {
  position: relative;
  display: inline-block;
}

.image-wrapper img {
  display: block;
  max-width: 100%;
  height: auto;
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
button.active {
  background-color: var(--active-color);
  border-color: var(--active-color);
  color: white;
}
</style>
