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
    explanation:
      'Comic panels are the essential frames through which stories unfold. Each panel captures a distinct moment, and together, they create a sequence of actions or emotions. Artists vary the size, shape, and layout of panels to influence pacing and emphasis, a large panel might spotlight a dramatic event, while smaller, tightly packed panels can heighten tension or quicken the story’s rhythm.'
  },
  {
    src: gutterImage,
    label: 'Gutter',
    explanation:
      'The gutter is the often-overlooked space between panels, but it plays a vital role in storytelling. This empty zone invites readers to fill in the gaps between scenes, imagining what happens in the transition. This process is called "closure," and it’s what transforms static images into a dynamic narrative in the reader’s mind.'
  },
  {
    src: bubbleImage,
    label: 'Speech Bubble',
    explanation:
      'Speech bubbles give voice to comic characters. These graphic elements carry dialogue, inner monologues, and sound effects, all while conveying tone through shape and design. A spiky bubble may indicate yelling, while a soft, cloud-like one might represent a thought. Speech bubbles also guide the reader’s eye across the page and define the rhythm of conversations.'
  },
  {
    src: entityImage,
    label: 'Entities (Characters & Objects)',
    explanation:
      'Entities, such as characters, props, and symbols,  are the visual anchors of each comic panel. They convey plot, emotion, and personality. Artists use body language, facial expressions, and spatial composition to highlight these elements. Understanding how entities are depicted and emphasized helps in decoding the scene and following the story’s emotional beats.'
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
