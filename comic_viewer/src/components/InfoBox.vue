<template>
  <div class="container">
    <ImageExplanationViewer :images="images" :title="title" />
  </div>
</template>

<script setup>
import ImageExplanationViewer from "./ImageExplanationViewer.vue";
import Normal from "../assets/Normal.jpg"
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
    explanation: `According to the World Health Organization, about 2.2 billion people worldwide live with some form of near- or distance-vision loss...`,
    src: Normal,
  },
  {
    label: "Medium Visual Impairment",
    explanation: `Medium visual impairment is characterised by pervasive blur rather than lost fields of vision...`,
    src: Mediocore,
  },
  {
    label: "Severe Visual Impairment",
    explanation: `People with severe visual impairment often experience tunnel vision...`,
    src: Severe,
  }
];
</script>
