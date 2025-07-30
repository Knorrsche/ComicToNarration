<template>
  <div class="container">
    <h1>Visual Impairments</h1>
    <ImageExplanationViewer :images="images" />
  </div>
</template>

<script setup>
import ImageExplanationViewer from "../components/ImageExplanationViewer.vue";
import Normal from "../assets/Normal.jpg"
import Mediocore from "../assets/Mediocore.png"
import Severe from "../assets/Severe.png"

const images = [
{
  label: "No Visual Impairment",
  explanation: `According to the World Health Organization, about 2.2 billion people worldwide live with some form of near- or distance-vision loss. Given a global population of roughly 8 billion, that leaves an estimated 5.8 billion people, well over two-thirds, who do not have a clinically significant visual impairment.

For this cohort, the hybrid language of graphic novels can be enjoyed as its creators intend: readers can effortlessly parse facial micro-expressions, colour symbolism, panel transitions, and onomatopoeic lettering without assistive technology.
But this doesnt mean there is no direct benefit for them, more inclusive options also widen the possibilities for all, such as more sophisticated audiobooks, that are able to parse the interweaved narrative of graphic novels.`,
  src: Normal,
},
  {
    label: "Medium Visual Impairment",
    explanation:
      `Medium visual impairment is characterised by pervasive blur rather than lost fields of vision. Fine print dissolves, facial features beyond a few metres smear together, and low‑contrast artwork becomes muddy. Readers can still follow overall page layout and large colour blocks, but dialog balloons and subtle facial cues fade unless magnified or viewed under bright, high‑contrast conditions.

      Common accommodations include handheld magnifiers, large‑print or re‑flowable digital editions, and adjustable‑contrast e‑ink screens. The International Agency for the Prevention of Blindness estimates that over 200 million people fall into this moderate vision loss band, making it the most prevalent tier of low vision worldwide.`,
    src: Mediocore,
  },
  {
    label: "Severe Visual Impairment",
    explanation:
      `People with severe visual impairment often experience tunnel vision, where only a narrow field is sharp and everything else falls away into darkness. In the example image, only the centre of the scene is discernible while the rest is dimmed and blurred.

      At this level , even large text is difficult to read and peripheral detail is lost. Speech bubbles may be unreadable; artwork collapses into vague silhouettes unless it is extremely high‑contrast or enlarged. Globally, around 36 million people are completely blind and 217 million live with moderate‑to‑severe vision loss. Many require screen readers, audio description, or tactile graphics to access visual media.`,
    src: Severe,
  }
];

</script>