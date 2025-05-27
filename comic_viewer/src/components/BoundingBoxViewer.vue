<template>
  <div class="outer-container">
    <input type="file" @change="handleFileChange" accept="image/*" />
    <h1>Deep Learning</h1>
    <!-- Only show buttons and image-wrapper if imageSrc is set -->
    <div v-if="imageSrc">
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
  </div>
</template>


<script setup>
import { ref, computed } from "vue";

const imageSrc = ref("");
const imageRef = ref(null);
const boundingBoxes = ref([]);

const showPanels = ref(true);
const showBubbles = ref(true);
const showEntities = ref(true);

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

const extractBoxesFromXml = (xmlDoc) => {
  const boxes = [];
  const collect = (tag, type) => {
    const nodes = xmlDoc.getElementsByTagName(tag);
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
  return boxes;
};

const fetchImageAndBoxes = async (file) => {
  try {
    const formData = new FormData();
    formData.append("file", file);

    const response = await fetch("http://localhost:8000/get-comic", {
      method: "POST",
      body: formData,
    });

    if (!response.ok) throw new Error("Failed to fetch comic data");

    const data = await response.json();

    imageSrc.value = `data:image/png;base64,${data.image}`;

    const parser = new DOMParser();
    const xmlDoc = parser.parseFromString(data.annotations, "application/xml");

    boundingBoxes.value = extractBoxesFromXml(xmlDoc);
  } catch (error) {
    console.error("Error loading comic data:", error);
  }
};

const boxStyle = (box) => ({
  top: `${box.y * scaleY.value}px`,
  left: `${box.x * scaleX.value}px`,
  width: `${box.width * scaleX.value}px`,
  height: `${box.height * scaleY.value}px`,
  position: "absolute",
});

const scaleX = ref(1);
const scaleY = ref(1);

const onImageLoad = () => {
  const img = imageRef.value;
  if (!img) return;

  scaleX.value = img.clientWidth / img.naturalWidth;
  scaleY.value = img.clientHeight / img.naturalHeight;
};

const handleFileChange = (event) => {
  const file = event.target.files[0];
  if (file) {
    fetchImageAndBoxes(file);
  }
};
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
