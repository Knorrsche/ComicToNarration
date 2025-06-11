<script setup>
import example2 from '../assets/Spider_chapter.png';
import example_mp4 from '../assets/Example_Video.mp4';

</script>

<template>
  <header class="header">
    <h1>Descriptive Narration of Comics</h1>
    <h2>Enhancing the Accessibility for the Visually Impaired</h2>

    <div class="example-images">
      <video controls playsinline muted preload="metadata" tabindex="0">
        <source :src="example_mp4" type="video/mp4" />
        Your browser does not support the video tag.
      </video>
      <img :src="example2" alt="Example 2" />
    </div>
  </header>
<h2>Welcome to the Comic Analysis Research Page at CAIRO THWS.</h2>
<p>This page provides an introduction to the field, along with key insights and challenges related to the interaction between comics and individuals with visual impairments.</p>

</template>

<style scoped>
.header {
  padding: 20px;
  background-color: #fff;
  border-bottom: 1px solid #ccc;
  box-sizing: border-box;
}

h1 {
  margin-bottom: 0.25em;
  font-size: clamp(1.8rem, 4vw, 2.4rem);
  font-weight: 700;
  color: #222;
}

h2 {
  margin-top: 0;
  margin-bottom: 1.5em;
  font-weight: 500;
  color: #555;
  font-size: clamp(1.1rem, 2.5vw, 1.4rem);
    font-family: Tahoma, sans-serif;

}
p{
    font-family: Tahoma, sans-serif;

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
  border-radius: 4px;
  object-fit: contain;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}



@media (max-width: 768px) {
  .example-images {
    flex-direction: column;
    gap: 15px;
  }
}
</style>
