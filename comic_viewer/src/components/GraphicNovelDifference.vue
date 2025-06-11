<script setup>
import example1 from '../assets/Spiderman.jpg';
import example2 from '../assets/vagabond.jpg';
import example3 from '../assets/Graphic_Novel.png';
import ImageExplanationViewer from '../components/ImageExplanationViewer.vue';

const images = [
  {
    src: example1,
    label: 'Western Comic',
    explanation: 'This image shows a typical panel from a Western comic, characterized by colorful art, dynamic action scenes, and left-to-right text flow. Western comics often use bold line art, speech bubbles with dramatic fonts, and a clear panel sequence. They tend to emphasize superhero narratives, satire, or dramatic fiction. Marvel and DC Comics are well-known examples of this style, which has roots in American pulp magazines and Sunday newspaper strips.'
  },
  {
    src: example2,
    label: 'Japanese Manga',
    explanation: 'This image depicts a panel from a Japanese manga, traditionally printed in black and white with a top-to-bottom, right-to-left reading order. Manga uses intricate line work, expressive facial features, and stylized sound effects. Genres are diverse, ranging from action (shōnen) to romance, slice-of-life, and psychological thrillers. Unlike Western comics, manga is often serialized in weekly or monthly magazines and places heavy emphasis on pacing and emotional nuance.'
  },
  {
    src: example3,
    label: 'Other Graphic Novels',
    explanation: 'This image represents newer or alternative formats in graphic storytelling. These might include European bandes dessinées (e.g., Tintin, Asterix), webtoons designed for vertical scrolling, or indie graphic novels that experiment with layout, color, and themes. Unlike traditional comics, these works often aim for artistic expression, personal narratives, or political commentary. The format has grown to include hybrid styles and digital-first media, expanding the boundaries of visual literature.'
  }
];

</script>

<template>
  <div class="container">
    <h1>Types of Graphic Novels</h1>
    <ImageExplanationViewer :images="images" />
  </div>
</template>
