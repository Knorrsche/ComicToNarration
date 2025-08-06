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
    explanation: `Comic panels are the building blocks of visual storytelling. Each one captures a frozen moment in time, a single beat of the narrative, while the arrangement of multiple panels creates a sense of motion and continuity. Artists use panel size, shape, and placement to control pacing and emphasis: a full-page panel can stop the reader in awe, while a sequence of small, narrow panels can quicken the rhythm and heighten urgency. In essence, panels are where the story comes to life, one frame at a time.

Challenges for the Visually Impaired:
Identifying panel boundaries can be difficult, especially when lines are faint, overlapping, or blended into complex backgrounds. This can make it hard to follow the reading order.

Challenges for AI:
AI often struggles with irregular panel shapes, creative layouts that break the grid, or panels without clear borders, making segmentation harder.`
  },
  {
    src: bubbleImage,
    label: 'Speech Bubble',
    explanation: `Speech bubbles are the voices of the comic world. They not only carry dialogue, inner thoughts, and sound effects but also express tone and emotion through their design. A jagged bubble might explode with anger or urgency, while a cloud-like one floats gently with introspection. Beyond their visual flair, speech bubbles act as guides for the reader’s eyes, leading them from one moment to the next and setting the rhythm of conversations across the page.

Challenges for the Visually Impaired:
Text inside bubbles may be too small or low-contrast to read, and irregular bubble shapes can make text extraction harder for assistive tools.

Challenges for AI:
Bubbles can overlap artwork, vary greatly in style, or be handwritten, making automated detection and text recognition challenging.`
  },
  {
    src: entityImage,
    label: 'Entities (Characters & Objects)',
    explanation: `Entities, whether characters, objects, or symbolic elements, are the focal points of each panel. They carry the story’s action, emotion, and personality. Artists convey their importance through body language, facial expressions, framing, and positioning within the scene. Even small background details can speak volumes, adding depth to the world and enriching the reader’s understanding of the moment. Recognizing how these elements interact is key to fully appreciating a comic’s narrative and emotional beats.

Challenges for the Visually Impaired:
Characters and objects may be hard to distinguish from the background if contrast is low or if details are too fine, leading to confusion about the scene.

Challenges for AI:
AI struggles with highly stylized characters, overlapping objects, and varying art styles, which can cause misclassification or missed detections.`
  },
  {
    src: gutterImage,
    label: 'Gutter',
    explanation: `The gutter, the empty space between panels, is where much of the story’s unseen action takes place. It represents the moments between the moments, requiring readers to mentally fill in events, movements, and emotional beats that are not explicitly drawn. This imaginative leap, known as "closure", is essential to comic storytelling.

Challenges for the Visually Impaired:
Without access to the visual cues of the surrounding panels, imagining or understanding what happens in the gutter can be especially challenging. Missing or unclear descriptions of these in-between moments can break the flow of the story.

Challenges for AI:
AI cannot truly “imagine” what happens between panels, it can only infer based on detected objects, characters, and context. Creative or ambiguous storytelling makes it even harder for AI to guess the intended narrative between frames.`
  }
];

const props = defineProps({
  title: {
    type: String,
    required: true
  }
});
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
