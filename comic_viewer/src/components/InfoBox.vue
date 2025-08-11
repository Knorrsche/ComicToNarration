<template>
  <div class="container">
    <ImageExplanationViewer :images="images" :title="title" />
  </div>
</template>

<script setup>
import ImageExplanationViewer from "./ImageExplanationViewer.vue";
import Normal from "../assets/Normal.png"
import Mediocore from "../assets/Mediocore.png"
import Severe from "../assets/Severe.png"

const props = defineProps({
  title: {
    type: String,
    required: true
  }
})

const images = [
  {
    label: "No Visual Impairment",
    explanation: `A reader with no visual impairment experiences comics exactly as intended by the artist: crisp line work, vivid and accurate colors, and full visibility of every panel’s composition.
    Speech bubbles are sharp and easy to read, even in smaller fonts, and fine details in the artwork, such as subtle facial expressions or intricate background elements, are easily noticed. Page layouts flow naturally, with no visual barriers interrupting the pacing of the story.
    The richness of the medium, from fine ink textures to nuanced shading, is fully appreciated, making reading smooth, comfortable, and immersive.`,
    src: Normal,
  },
  {
    label: "Medium Visual Impairment",
    explanation: `With medium visual impairment, the experience of reading comics changes noticeably. The entire page appears slightly blurred, making it harder to read small or stylized fonts without magnification. Fine background details and delicate line art can be lost, and characters may appear less distinct from their surroundings. Color gradients and subtle shading may blend together, reducing the emotional impact of certain scenes. Page navigation can be slower, as the reader may need to move the page closer to their eyes or use assistive tools to make out dialogue and panel transitions. While the overall story can still be followed, much of the visual richness that gives comics their unique style may be diminished.`,
    src: Mediocore,
  },
  {
    label: "Severe Visual Impairment",
    explanation: `For a comic reader with severe visual impairment, much of the visual storytelling becomes inaccessible without adaptation. Vision may be restricted to a small central field (tunnel vision) or reduced to vague shapes and colors, making it nearly impossible to identify characters, follow panel sequences, or read dialogue without assistive technology. The layout of a page may be difficult to navigate, especially when panels are arranged in unconventional patterns. Complex visual scenes can become overwhelming or indistinguishable, and the emotional nuance conveyed through facial expressions or detailed backgrounds may be completely lost. To enjoy comics, readers at this level may rely on audio descriptions, tactile graphics, or highly zoomed-in digital versions with screen reading software to convey text and describe imagery.`,
    src: Severe,
  }
];


</script>
