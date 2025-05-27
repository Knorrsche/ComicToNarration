<script setup>
import example1 from '../assets/Spider_image.png'
import example2 from '../assets/Spider_chapter.png'
import example_mp4 from '../assets/Example_Video.mp4'
</script>
<template>
  <header class="header">
    <h1>Descriptive Narration of Comics</h1>
    <h2>Enhancing the Accessibility for the Visually Impaired</h2>
  <div class="example-images">
          <video controls playsinline>
<source :src="example_mp4" type="video/mp4" />
        Your browser does not support the video tag.
      </video>
    <img :src="example2" alt="Example 2" />
  </div>
    <div>

    </div>
  </header>
</template>

<style scoped>
.header {
  padding: 20px;
  background-color: #fff;
  border-bottom: 1px solid #ccc;
}

.example-images {
  display: flex;
  gap: 20px;
  align-items: center;
}

.example-images img,
.example-images video {
  max-width: 500px;
  width: 100%;
  height: auto;
  border-radius: 4px;
  object-fit: contain;
}
</style>
