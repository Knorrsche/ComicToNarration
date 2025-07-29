<template>
  <div class="outer-container">
    <h1>Deep Learning</h1>
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
      </div>
      <ComicScrollPanel></ComicScrollPanel>
    </div>
  </div>
</template>

<script setup>
import ComicScrollPanel from "../components/ComicScrollPanel.vue";

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

.image-wrapper img {
  width: 100%;
  height: auto;
  object-fit: contain;
  border-radius: 6px;
  box-shadow: 0 0 12px rgba(0, 0, 0, 0.2);
  user-select: none;
  display: block;
}


</style>