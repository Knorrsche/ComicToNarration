<script setup>
import example2 from '../assets/Spider_chapter.png';
import example_mp4 from '../assets/Example_Video.mp4';

const props = defineProps({
  title: {
    type: String,
    required: true
  }
});
</script>

<template>
  <header class="header">
    <div class="header-content">
      <h1>Descriptive Narration of Comics</h1>
      <h2>Enhancing the Accessibility for the Visually Impaired</h2>

      <div class="example-images">
        <video controls playsinline preload="metadata" tabindex="0">
          <source :src="example_mp4" type="video/mp4" />
          Your browser does not support the video tag.
        </video>
        <img :src="example2" alt="Example 2" />
      </div>
    </div>
  </header>
</template>

<style scoped>
.header {
  display: flex;
  justify-content: center;  /* Horizontal center */
  align-items: center;      /* Vertical center */
  min-height: 100vh;        /* Take full screen height */
  padding: 2rem;
  background: linear-gradient(135deg, #ffffff, #f8f8f8);
  box-sizing: border-box;
}

.header-content {
  text-align: center;
  max-width: 1200px;
  background: #fff;
  padding: 2rem;
  border-radius: 16px;
  box-shadow: 0 4px 20px rgba(0,0,0,0.06);
}

h1 {
  margin-bottom: 0.25em;
  font-size: clamp(1.8rem, 4vw, 2.4rem);
  font-weight: 700;
  color: #222;
  font-family: "Inter", "Segoe UI", Tahoma, sans-serif;
}

h2 {
  margin-top: 0;
  margin-bottom: 1.5em;
  font-weight: 500;
  color: #555;
  font-size: clamp(1.1rem, 2.5vw, 1.4rem);
  font-family: "Inter", "Segoe UI", Tahoma, sans-serif;
}

.example-images {
  display: flex;
  flex-wrap: nowrap;
  gap: 20px;
  align-items: center;
  justify-content: center;
  margin-bottom: 20px;
}

.example-images img,
.example-images video {
  max-width: 500px;
  width: 100%;
  height: auto;
  border-radius: 12px;
  object-fit: contain;
  box-shadow: 0 4px 14px rgba(0, 0, 0, 0.08);
  background: #fff;
}

@media (max-width: 768px) {
  .example-images {
    flex-direction: column;
    gap: 15px;
  }

  .header-content {
    padding: 1.2rem;
    border-radius: 12px;
  }
}
</style>
