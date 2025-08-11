<script setup>
import example1 from '../assets/Normal.png';
import example2 from '../assets/Manga_image.png';
import example3 from '../assets/GraphicNovel.png';
import ImageExplanationViewer from './ImageExplanationViewer.vue';

const props = defineProps({
  title: {
    type: String,
    required: true
  }
})

const images = [
  {
    label: "Western Comic",
    explanation: `Western comics are a vibrant blend of dynamic action, bold colors, and dramatic storytelling. Pages are designed for left-to-right reading, with panels flowing in a clear, sequential order. Speech bubbles often feature strong, stylized fonts that match the energy of the scene, while bold line work and striking color palettes make every moment feel larger than life.

    Traditionally rooted in superhero adventures, satire, and dramatic fiction, this style has deep ties to American pulp magazines and newspaper strips of the early 20th century. Iconic publishers like Marvel and DC have shaped the genre into a visual language of action and heroism, where every panel feels like a snapshot of epic storytelling.`,
    src: example1
  },
  {
    label: "Japanese Manga",
    explanation: `Japanese manga offers a reading experience steeped in mood, pacing, and emotional nuance. Presented in black and white, it flows from right to left and top to bottom, immersing the reader in a rhythm unique to the medium. Line work ranges from delicate to intense, capturing everything from explosive battles to quiet, introspective moments.

    Manga excels at expressive character design, with eyes, gestures, and panel framing often carrying as much weight as the dialogue. Genres are incredibly diverse,spanning action-packed shōnen adventures, heartfelt romance, contemplative slice-of-life, and thought-provoking psychological tales. Most manga begins as serialized chapters in weekly or monthly magazines, gradually building immersive worlds where storytelling and atmosphere intertwine.`,
    src: example2
  },
  {
    label: "Other Graphic Novels",
    explanation: `Beyond the traditional realms of Western comics and manga lies a vast spectrum of graphic storytelling. This category embraces everything from European bandes dessinées, with their richly detailed art and adventurous spirit, to vertically scrolling webtoons designed for modern digital screens. Indie and experimental graphic novels push boundaries even further, playing with unconventional layouts, bold color theory, and themes ranging from deeply personal memoirs to political critique.

    These works often prioritize artistic exploration and narrative experimentation over strict genre conventions. Whether printed on paper or crafted for a digital-first audience, they challenge the definition of a "comic," expanding the medium into new spaces where visuals and text merge into limitless forms of expression.`,
    src: example3
  }
];
</script>

<template>
  <div class="container">
    <ImageExplanationViewer :images="images" :title="title" />
  </div>
</template>
