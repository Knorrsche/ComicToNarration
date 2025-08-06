<script setup>
import panelImage from '../assets/panel.png';
import gutterImage from '../assets/scene.png';
import bubbleImage from '../assets/speaking_type.png';
import entityImage from '../assets/crowded_entity.png';
import ImageExplanationViewer from './ImageExplanationViewer.vue';

const concepts = [
  {
    src: panelImage,
    label: 'Comic Panel',
    explanation: `Comic panels are the building blocks of visual storytelling. Each one captures a frozen moment in time, a single beat of the narrative, while the arrangement of multiple panels creates a sense of motion and continuity. Artists use panel size, shape, and placement to control pacing and emphasis: a full-page panel can stop the reader in awe, while a sequence of small, narrow panels can quicken the rhythm and heighten urgency. In essence, panels are where the story comes to life, one frame at a time.`
  },
  {
    src: gutterImage,
    label: 'Gutter',
    explanation: `The gutter, the empty space between panels, may seem insignificant, but it is where much of the magic of comics happens. This gap represents a pause in the visual sequence, prompting readers to imagine what occurs between the depicted moments. This mental process, known as "closure," transforms a static series of images into a continuous, living story. In skilled hands, the gutter becomes an invisible storyteller, shaping tension, surprise, and emotional impact without ever showing a single line.`
  },
  {
    src: bubbleImage,
    label: 'Speech Bubble',
    explanation: `Speech bubbles are the voices of the comic world. They not only carry dialogue, inner thoughts, and sound effects but also express tone and emotion through their design. A jagged bubble might explode with anger or urgency, while a cloud-like one floats gently with introspection. Beyond their visual flair, speech bubbles act as guides for the reader’s eyes, leading them from one moment to the next and setting the rhythm of conversations across the page.`
  },
  {
    src: entityImage,
    label: 'Entities (Characters & Objects)',
    explanation: `Entities, whether characters, objects, or symbolic elements, are the focal points of each panel. They carry the story’s action, emotion, and personality. Artists convey their importance through body language, facial expressions, framing, and positioning within the scene. Even small background details can speak volumes, adding depth to the world and enriching the reader’s understanding of the moment. Recognizing how these elements interact is key to fully appreciating a comic’s narrative and emotional beats.`
  }
];

const props = defineProps({
  title: {
    type: String,
    required: true
  }
})
</script>

<template>
  <div class="container">
    <ImageExplanationViewer :images="concepts" :title="title" />
  </div>
</template>

<style scoped>
.container {
  padding: 0rem;
  width: 100%;
  height: 100%;
  box-sizing: border-box;
}
</style>
