<template>
  <div class="container">
    <input type="file" accept="image/*" @change="handleFileChange" />
    <h1>Perspective of the Visualy Impaired</h1>
    <div v-if="images.length" class="viewer">
      <div class="explanation-box">
        <h3>Explanation</h3>
        <p>{{ explanations[currentIndex] || "No explanation available." }}</p>
      </div>

      <div class="image-viewer">
        <button class="nav-button" @click="prevImage" :disabled="currentIndex === 0">◀</button>

        <div class="image-container">
          <img :src="images[currentIndex].base64" :alt="images[currentIndex].label" />
          <div class="caption">{{ images[currentIndex].label }}</div>
        </div>

        <button class="nav-button" @click="nextImage" :disabled="currentIndex === images.length - 1">▶</button>
      </div>
    </div>

    <div v-else class="placeholder">
      Upload an image to see transformed versions
    </div>
  </div>
</template>

<script setup>
import { ref } from "vue";

const images = ref([]);
const currentIndex = ref(0);
const explanations = ref([]);

const handleFileChange = async (event) => {
  const file = event.target.files[0];
  if (!file) return;

  images.value = [];
  explanations.value = [];
  currentIndex.value = 0;

  const reader = new FileReader();
  reader.readAsDataURL(file);

  reader.onload = () => {
    const originalSrc = reader.result;

    // Create an offscreen image to process
    const img = new Image();
    img.src = originalSrc;
    img.onload = () => {
  const width = img.width;
  const height = img.height;

  // Blurred canvas (same as before)
  const canvasBlur = document.createElement("canvas");
  canvasBlur.width = width;
  canvasBlur.height = height;
  const ctxBlur = canvasBlur.getContext("2d");
  ctxBlur.filter = "blur(8px)";
  ctxBlur.drawImage(img, 0, 0, width, height);

  // Black with holes (holes show original image)
  const canvasBlackHoles = document.createElement("canvas");
  canvasBlackHoles.width = width;
  canvasBlackHoles.height = height;
  const ctxBlackHoles = canvasBlackHoles.getContext("2d");

  // Draw original image first
  ctxBlackHoles.drawImage(img, 0, 0, width, height);

  // Overlay black rectangle
  ctxBlackHoles.fillStyle = "black";
  ctxBlackHoles.fillRect(0, 0, width, height);

  // Punch holes in black overlay (clear circles to show original)
  ctxBlackHoles.globalCompositeOperation = "destination-out";
  const holeCount = 100;
  const holeRadius = Math.min(width, height) / 40;
  for (let i = 0; i < holeCount; i++) {
    const x = Math.random() * width;
    const y = Math.random() * height;
    ctxBlackHoles.beginPath();
    ctxBlackHoles.arc(x, y, holeRadius, 0, Math.PI * 2);
    ctxBlackHoles.fill();
  }
  ctxBlackHoles.globalCompositeOperation = "source-over";

  // Complete black canvas (same as before)
  const canvasBlack = document.createElement("canvas");
  canvasBlack.width = width;
  canvasBlack.height = height;
  const ctxBlack = canvasBlack.getContext("2d");
  ctxBlack.fillStyle = "black";
  ctxBlack.fillRect(0, 0, width, height);

  images.value = [
    {
      label: "Blurred Image",
      base64: canvasBlur.toDataURL(),
    },
    {
      label: "Black with Small Holes",
      base64: canvasBlackHoles.toDataURL(),
    },
    {
      label: "Complete Black",
      base64: canvasBlack.toDataURL(),
    },
  ];

explanations.value = [
  "This blurred version simulates mild to moderate visual impairment, such as nearsightedness or early cataracts, where details become fuzzy and hard to distinguish. Around 217 million people worldwide experience this level of visual difficulty, which affects daily tasks like reading and recognizing faces.",

  "This black overlay with small holes reveals glimpses of the original image underneath, representing severe visual impairment characterized by 'tunnel vision' or partial sight loss. Conditions like glaucoma cause a loss of peripheral vision, making it challenging to navigate surroundings. Approximately 36 million people globally live with severe vision impairment or blindness, many with this form of partial vision.",

  "This completely black image depicts total blindness, where no visual information is perceived. People with complete vision loss rely on other senses for interaction and independence. About 43 million people worldwide are blind, emphasizing the importance of accessible tools and descriptions to aid their daily lives."
];

};

  };
};

const prevImage = () => {
  if (currentIndex.value > 0) currentIndex.value--;
};

const nextImage = () => {
  if (currentIndex.value < images.value.length - 1) currentIndex.value++;
};
</script>

<style scoped>
.container {
  max-width: 900px;
  margin: 20px auto;
  font-family: Arial, sans-serif;
  text-align: center;
}

input[type="file"] {
  margin-bottom: 15px;
}

.viewer {
  display: flex;
  align-items: flex-start;
  gap: 20px;
  justify-content: center;
}

.explanation-box {
  flex: 1 1 300px;
  padding: 15px;
  background-color: #f9f9f9;
  border-radius: 8px;
  box-shadow: 0 0 8px rgba(0,0,0,0.1);
  text-align: left;
  user-select: none;
  min-height: 400px;
}

.explanation-box h3 {
  margin-bottom: 10px;
  font-size: 1.3rem;
  color: #444;
}

.explanation-box p {
  font-size: 1rem;
  color: #555;
  line-height: 1.4;
}

.image-viewer {
  display: flex;
  align-items: center;
  gap: 10px;
}

.nav-button {
  background-color: #007bff;
  color: white;
  border: none;
  padding: 10px 15px;
  font-size: 1.3rem;
  cursor: pointer;
  border-radius: 5px;
  user-select: none;
}

.nav-button:disabled {
  background-color: #ccc;
  cursor: not-allowed;
}

.image-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  max-width: 400px;
  max-height: 400px;
  width: 100%;
  overflow: visible;
}

.image-container img {
  max-width: 100%;
  max-height: 400px;
  border-radius: 6px;
  object-fit: contain;
  box-shadow: 0 0 12px rgba(0, 0, 0, 0.2);
  margin-bottom: 8px;
}

.caption {
  font-weight: bold;
  font-size: 1.1rem;
  color: #333;
  text-align: center;
  user-select: none;
}

.placeholder {
  color: #777;
  font-style: italic;
  margin-top: 50px;
}
</style>
