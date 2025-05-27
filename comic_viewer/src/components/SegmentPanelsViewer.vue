<template>
  <div class="container">
    <input type="file" accept="image/*" @change="handleFileChange" />
    <h1>Traditional Machine Learning</h1>
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
      Upload an image to see segmentation results
    </div>
  </div>
</template>

<script setup>
import { ref } from "vue";

const images = ref([]);
const currentIndex = ref(0);

const captions = {
  original: "Original Image",
  grayscale: "Grayscale",
  edges: "Canny Edges",
  dilated_edges: "Dilated Edges",
  filled: "Filled Holes",
  labeled: "Labeled Panels"
};

const explanations = ref([]);

const handleFileChange = async (event) => {
  const file = event.target.files[0];
  if (!file) return;

  images.value = [];
  explanations.value = [];
  currentIndex.value = 0;

  const formData = new FormData();
  formData.append("file", file);

  try {
    const response = await fetch("http://localhost:8000/segment-panels", {
      method: "POST",
      body: formData,
    });

    if (!response.ok) {
      throw new Error("Failed to segment panels");
    }

    const data = await response.json();

    const loadedImages = [];
    const loadedExplanations = [];

    for (const key of ["original", "grayscale", "edges", "dilated_edges", "filled", "labeled"]) {
      if (data[key]) {
        loadedImages.push({
          label: captions[key] || key,
          base64: `data:image/png;base64,${data[key]}`,
        });

switch (key) {
  case "original":
    loadedExplanations.push(
      "This is the original uploaded image, serving as the baseline for all processing steps."
    );
    break;
  case "grayscale":
    loadedExplanations.push(
      "Grayscale conversion simplifies the image by removing color information, which helps focus on intensity differences crucial for edge detection."
    );
    break;
  case "edges":
    loadedExplanations.push(
      "Edges are detected using the Canny edge detection algorithm, which highlights the boundaries between different regions by finding intensity gradients."
    );
    break;
  case "dilated_edges":
    loadedExplanations.push(
      "Dilation thickens the detected edges, connecting broken or thin lines to form continuous boundaries, which improves segmentation quality."
    );
    break;
  case "filled":
    loadedExplanations.push(
      "Filling holes closes gaps inside detected shapes, turning edge outlines into solid regions that represent individual panels or objects."
    );
    break;
  case "labeled":
    loadedExplanations.push(
      "Each connected region is labeled, assigning unique IDs to panels so they can be identified and extracted individually."
    );
    break;
  default:
    loadedExplanations.push("");
}

      }
    }



    images.value = loadedImages;
    explanations.value = loadedExplanations;
  } catch (error) {
    console.error("Error uploading file:", error);
  }
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
