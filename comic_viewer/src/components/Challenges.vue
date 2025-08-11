<script setup>
import entityMatch from '../assets/EntitiesMatched.png';
import speakerID from '../assets/Speaker_identi.png';
import sceneDetect from '../assets/Scenes.png';
import ImageExplanationViewer from './ImageExplanationViewer.vue';

const challenges = [
  {
src: entityMatch,
label: 'Entity Matching',
explanation: `Entity matching is the skill of recognizing the same character or object as they reappear throughout a comic, even when their appearance changes dramatically.

Shifts in perspective, new outfits, altered hairstyles, or varied facial expressions can all obscure identity. Overlapping or poorly defined bounding boxes make this task even more challenging.

For human readers, narrative context and intuition naturally bridge these visual gaps. For automated systems, it becomes a complex visual puzzle, one that requires combining both visual cues and story context to correctly link appearances.

Accurate entity matching preserves narrative continuity, keeping characters, relationships, and actions clear from panel to panel.`

  },
{
  src: speakerID,
  label: 'Speaker Identification',
  explanation: `Speaker identification is the process of determining which character is delivering a line of dialogue within a panel.

  Readers draw on a blend of clues: the direction and length of a speech bubble tail, the position of characters, subtle facial cues, or even a character’s posture and gaze.

In crowded scenes with overlapping bubbles, multiple speakers, or unclear bubble tails, this task becomes far more difficult. While humans naturally rely on logic and narrative context to fill in gaps, automated systems must disentangle a complex web of visual cues to correctly assign each voice.

AI often struggles when speech bubbles lack clear tails, when characters are partially obscured, or when visual cues conflict with the narrative flow, making accurate attribution challenging.`
},
{
  src: sceneDetect,
  label: 'Scene Detection',
  explanation: `Scene detection is the process of recognizing when the narrative shifts to a new place, time, or storyline.

  In comics, these transitions are often implied rather than directly stated, unfolding gradually over several panels. Artists may signal a change through subtle background alterations, a dramatic shift in color palette, or a restructured panel layout.

For readers, these visual cues work almost subconsciously, guiding them through the story without explicit markers. For automated systems, accurately identifying scene boundaries is essential to preserving narrative structure and understanding the sequence of events.

AI often struggles with unconventional transitions, abstract visual cues, or stories that blend locations and timelines without clear separators, making it difficult to pinpoint when one scene truly ends and another begins.`
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
