<template>
  <div class="outer-container">
    <h1>Deep Learning</h1>

    <div class="upload-box">
      <input type="file" accept="image/*" @change="handleUpload" />
    </div>

    <div v-if="loading" class="loading-overlay">Processing image...</div>

    <div class="content-wrapper">
      <div class="explanation-box">
        <h3>Deep Learning in Comics</h3>
        <p>
          Deep learning is a subset of machine learning that uses layered neural networks (like CNNs or transformers) to automatically learn features from large datasets. Unlike traditional machine learning, which requires handcrafted features (e.g. edge detectors or geometric rules), deep learning models learn directly from raw pixel data — enabling them to identify complex patterns in comic images.
        </p>
        <p>
          In the context of comics, deep learning allows automatic detection and interpretation of panels, speech bubbles, characters, and even emotions or narrative structure. This mimics how humans visually understand and follow stories, enabling smarter comic viewers and tools.
        </p>
        <p>
          <strong>Advantages:</strong> Deep learning models are highly flexible and robust to variation. They can handle diverse art styles, irregular layouts, and noisy backgrounds better than rule-based methods. With enough data, they generalize well across genres and languages, making them suitable for tasks like panel segmentation, speaker identification, or even automatic comic translation.
        </p>
        <p>
          <strong>Limitations:</strong> Deep learning systems require large labeled datasets and substantial computational resources to train. They can also be opaque ("black boxes"), making it hard to understand why a model made a certain decision — which is problematic for transparency or debugging. Additionally, if the training data is biased or limited, the system may fail to generalize.
        </p>
        <p>
          Despite these challenges, deep learning has revolutionized comic understanding, offering new possibilities for accessibility (e.g. visually impaired readers), creativity (e.g. style transfer, auto-colorization), and research (e.g. studying visual narratives at scale).
        </p>
        <p>
          Explore how AI models learn to recognize comic structure, enabling rich, interactive experiences that bring visual storytelling to life!
        </p>
      </div>

      <div class="right-panel">
        <div v-if="imageSrc">
          <div class="buttons">
            <button :class="{ active: showPanels }" @click="showPanels = !showPanels" style="--active-color: #007bff">Panels</button>
            <button :class="{ active: showBubbles }" @click="showBubbles = !showBubbles" style="--active-color: #dc3545">Speech Bubbles</button>
            <button :class="{ active: showEntities }" @click="showEntities = !showEntities" style="--active-color: #28a745">Entities</button>
          </div>

          <div class="image-wrapper" ref="wrapperRef">
            <img :src="imageSrc" @load="onImageLoad" ref="imageRef" alt="Processed comic" class="responsive-image" />
            <div v-for="(box, index) in filteredBoundingBoxes" :key="index" :class="['box-overlay', box.type]" :style="boxStyle(box)">
              <span class="label">{{ box.type }}</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted, nextTick } from "vue";

const imageSrc = ref("");
const imageRef = ref(null);
const wrapperRef = ref(null);
const boundingBoxes = ref([]);
const loading = ref(false);

const showPanels = ref(true);
const showBubbles = ref(true);
const showEntities = ref(true);

const imageWidth = ref(0);
const imageHeight = ref(0);
const scaleX = ref(1);
const scaleY = ref(1);

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

function dataURLtoBlob(dataurl) {
  const arr = dataurl.split(",");
  const mime = arr[0].match(/:(.*?);/)[1];
  const bstr = atob(arr[1]);
  let n = bstr.length;
  const u8arr = new Uint8Array(n);
  while (n--) u8arr[n] = bstr.charCodeAt(n);
  return new Blob([u8arr], { type: mime });
}

async function fetchImageAndBoxesFromBase64(base64DataUrl) {
  const blob = dataURLtoBlob(base64DataUrl);
  const file = new File([blob], "image.png", { type: blob.type });

  try {
    loading.value = true;
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

    await nextTick();
    updateScale();
  } catch (error) {
    console.error("Error loading comic data:", error);
  } finally {
    loading.value = false;
  }
}

function handleUpload(event) {
  const file = event.target.files[0];
  if (!file) return;

  const reader = new FileReader();
  reader.onload = () => {
    fetchImageAndBoxesFromBase64(reader.result);
  };
  reader.readAsDataURL(file);
}

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

onMounted(() => {
  window.addEventListener("resize", updateScale);
});

onUnmounted(() => {
  window.removeEventListener("resize", updateScale);
});
</script>
<style scoped>
.outer-container {
  max-width: 100%;
  min-height: 100vh;
  margin: 20px auto;
  padding: 20px;
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  box-sizing: border-box;
  font-family: Arial, sans-serif;
}

.upload-box {
  margin-bottom: 20px;
}

.loading-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  background: rgba(255, 255, 255, 0.85);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.5rem;
  color: #333;
  z-index: 9999;
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

.right-panel {
  height: 65vh;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: flex-start;
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

.image-wrapper {
  position: relative;
  width: 100%;
  max-width: 600px;
  height: auto;
  aspect-ratio: auto;
}

.image-wrapper img {
  width: 100%;
  height: auto;
  object-fit: contain;
  border-radius: 6px;
  box-shadow: 0 0 12px rgba(0, 0, 0, 0.2);
  user-select: none;
  display: block;
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
</style>