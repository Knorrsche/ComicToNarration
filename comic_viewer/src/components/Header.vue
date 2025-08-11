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
      <h1 class="main-title">
        Descriptive Narration of Comics
      </h1>
      <h2 class="subtitle">
        Enhancing the Accessibility for the Visually Impaired
      </h2>

      <div class="example-images">
        <div class="media-card">
          <video controls playsinline preload="metadata" tabindex="0">
            <source :src="example_mp4" type="video/mp4" />
            Your browser does not support the video tag.
          </video>
        </div>
        <div class="media-card">
          <img :src="example2" alt="Example 2" />
        </div>
      </div>

      <div class="scroll-indicator">↓ Scroll to Explore ↓</div>
    </div>
  </header>
</template>

<style scoped>
.header {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  padding: 2rem;
  background: none;
}

.header-content {
  text-align: center;
  max-width: 1200px;
  background: rgba(255, 255, 255, 0.85);
  padding: 2.5rem;
  border-radius: 20px;
  backdrop-filter: blur(10px);
  box-shadow: 0 8px 30px rgba(0,0,0,0.1);
  animation: fadeInUp 0.8s ease forwards;
}

.main-title {
  margin-bottom: 0.25em;
  font-size: clamp(2rem, 5vw, 3rem);
  font-weight: 800;
  font-family: "Inter", "Segoe UI", Tahoma, sans-serif;
  background: linear-gradient(90deg, #ff7f50, #ff4f81);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  letter-spacing: 0.5px;
}

.subtitle {
  margin-top: 0;
  margin-bottom: 2em;
  font-weight: 500;
  color: #555;
  font-size: clamp(1.2rem, 2.5vw, 1.5rem);
  animation: fadeIn 1.2s ease forwards;
}

.example-images {
  display: flex;
  flex-wrap: nowrap;
  gap: 20px;
  align-items: center;
  justify-content: center;
  margin-bottom: 30px;
  flex-wrap: wrap;
}

.media-card {
  background: white;
  border-radius: 16px;
  overflow: hidden;
  box-shadow: 0 8px 24px rgba(0,0,0,0.08);
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}
.media-card:hover {
  transform: translateY(-6px) scale(1.02);
  box-shadow: 0 12px 30px rgba(0,0,0,0.12);
}

.media-card img,
.media-card video {
  max-width: 500px;
  width: 100%;
  height: auto;
  display: block;
}

.scroll-indicator {
  font-size: 3rem;
  font-weight: 500;
  color: #FF7F50FF;
  animation: bounce 2s infinite;
}

@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}
@keyframes fadeInUp {
  from { opacity: 0; transform: translateY(20px); }
  to { opacity: 1; transform: translateY(0); }
}
@keyframes bounce {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-5px); }
}

@media (max-width: 768px) {
  .example-images {
    flex-direction: column;
    gap: 15px;
  }

  .header-content {
    padding: 1.5rem;
    border-radius: 14px;
  }
}
</style>
