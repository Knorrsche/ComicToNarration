<script setup>
import entityMatch from '../assets/clustering.png';
import speakerID from '../assets/speaker_iden.png';
import sceneDetect from '../assets/scene.png';
import ImageExplanationViewer from './ImageExplanationViewer.vue';

const challenges = [
  {
    src: entityMatch,
    label: 'Entity Matching',
    explanation: `Entity matching is the art of recognizing the same character or object as they reappear throughout a comic, even when their look changes dramatically. Perspective shifts, new outfits, altered hairstyles, or varied facial expressions can all obscure identity. For human readers, narrative context and intuition fill in the gaps, but for automated systems, this is a demanding visual puzzle. Accurate entity recognition ensures narrative continuity, allowing the story’s threads, relationships, and actions to remain clear from panel to panel.`
  },
  {
    src: speakerID,
    label: 'Speaker Identification',
    explanation: `Speaker identification is the process of determining which character is delivering a line of dialogue within a panel. Readers draw on a blend of clues: the direction and length of a speech bubble tail, the position of characters, subtle facial cues, or even a character’s posture and gaze. In crowded scenes with overlapping bubbles or multiple speakers, this becomes much trickier. While humans naturally rely on logic and context, algorithms must disentangle a web of visual signals to correctly assign each voice to its speaker.`
  },
  {
    src: sceneDetect,
    label: 'Scene Detection',
    explanation: `Scene detection is about recognizing when the narrative shifts to a new place, time, or storyline. In comics, these transitions are often implied rather than directly stated, unfolding over several panels. Artists may signal a scene change through a shift in background details, a dramatic color palette change, or an alteration in panel structure. For readers, these cues work subconsciously; for computational systems, detecting scene boundaries is critical to preserving the story’s structure and making sense of its unfolding events.`
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
