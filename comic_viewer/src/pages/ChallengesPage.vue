<script setup>
import entityMatch from '../assets/clustering.png';
import speakerID from '../assets/speaker_iden.png';
import sceneDetect from '../assets/scene.png';
import ImageExplanationViewer from '../components/ImageExplanationViewer.vue';

const challenges = [
  {
    src: entityMatch,
    label: 'Entity Matching',
    explanation:
      'Entity matching is the task of identifying and tracking the same character or object across multiple comic panels, even as their appearance shifts due to changes in perspective, pose, clothing, or expression. While humans use intuition and narrative context to resolve these variations, it poses a major hurdle for automated systems. Consistent entity recognition is crucial for maintaining narrative continuity and understanding character actions over time.'
  },
  {
    src: speakerID,
    label: 'Speaker Identification',
    explanation:
      'Determining who is speaking in a comic panel requires interpreting a mix of visual cues, such as the direction of speech bubble tails, character positioning, facial expressions, or even gaze. In complex scenes with overlapping bubbles or multiple speakers, ambiguity often arises. While readers can rely on narrative logic and context, algorithms frequently struggle with this task, making speaker identification a significant challenge in comic understanding.'
  },
  {
    src: sceneDetect,
    label: 'Scene Detection',
    explanation:
      'Scene detection involves recognizing when a comic shifts to a new setting, time period, or narrative thread. These transitions may span multiple panels and are often implied rather than explicitly marked. Artists use subtle signals such as background changes, color palette shifts, or layout transformations. For readers and especially for computational systems, accurately detecting scene boundaries is vital for maintaining a coherent understanding of the story’s structure.'
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
    <ImageExplanationViewer :images="challenges" :title="title" />
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
