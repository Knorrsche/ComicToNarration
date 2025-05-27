<script setup>
import Header from './components/Header.vue'
import InfoBox from "./components/InfoBox.vue";
import GraphicNovelDifference from "./components/GraphicNovelDifference.vue";
import ComicParts from "./components/ComicParts.vue";
import Challenges from "./components/Challenges.vue";
import SegmentPanelsViewer from './components/SegmentPanelsViewer.vue'
import BoundingBoxViewer from './components/BoundingBoxViewer.vue'
</script>

<template>
  <div class="page-container">
    <Header />

    <section class="top-section">
      <InfoBox></InfoBox>
    </section>

        <section class="top-middle-section">
      <GraphicNovelDifference></GraphicNovelDifference>
    </section>

    <section class="middle-middle-section">
      <ComicParts></ComicParts>
    </section>


    <section class="middle-middle-middle-section">
      <Challenges></Challenges>
    </section>

    <section class="middle-section">
      <SegmentPanelsViewer />
    </section>

    <section class="bottom-section">
      <BoundingBoxViewer />
    </section>
  </div>
</template>
