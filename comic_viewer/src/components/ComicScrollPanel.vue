<script setup>
import { useRouter } from 'vue-router';
import { nextTick, onMounted, ref } from "vue";

const router = useRouter();

const comicList = ref([]);
const selectedComic = ref(null);
const selectedPage = ref(null);

const goToViewer = (comicName) => {
  router.push({ path: `/viewer/${comicName}` });
};

const selectComic = (comic) => {
  selectedComic.value = comic;
  selectedPage.value = comic.pages[0];
  loadPage(comic.name, selectedPage.value);
};

const selectPage = (page) => {
  selectedPage.value = page;
  loadPage(selectedComic.value.name, page);
};

const loadPage = async (comicName, pageFilename) => {
  try {
    const response = await fetch(
      `https://projects.cairo.thws.de/comic-page?comic=${encodeURIComponent(comicName)}&page=${encodeURIComponent(pageFilename)}`
    );
    if (!response.ok) throw new Error("Failed to load comic page");

    const data = await response.json();
    imageSrc.value = `data:${data.mimeType};base64,${data.image}`;

    const parser = new DOMParser();
    const xmlDoc = parser.parseFromString(data.annotations, "application/xml");
    boundingBoxes.value = extractBoxesFromXml(xmlDoc);

    await nextTick();
  } catch (err) {
    console.error("Error loading page:", err);
  }
};

onMounted(async () => {
  try {
    const res = await fetch('https://projects.cairo.thws.de/api/comics') ;
    if (!res.ok) throw new Error("Failed to fetch comics");
    comicList.value = await res.json();
  } catch (err) {
    console.error("Error loading comic list:", err);
  }

});
</script>

<template>
  <div class="comic-scroll-panel">
    <div class="panel-title">
      Select a Comic
    </div>

    <div class="scroll-container">
      <div
        v-for="(comic, index) in comicList"
        :key="index"
        class="comic-card"
        @click="goToViewer(comic.name)"
      >
        <img
          :src="`https://projects.cairo.thws.de/api/comics/${comic.name}/${comic.pages[0]}`"
          alt="preview"
          class="comic-thumbnail"
        />
        <div class="comic-name">{{ comic.name }}</div>
      </div>
    </div>
  </div>
</template>

<style scoped>
:root {
  --orange: #da7434;
  --orange-hover: #c45d1f;
}

.comic-scroll-panel {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  height: 100%;
  max-height: 75vh;
  background: linear-gradient(135deg, rgba(255,255,255,0.85), rgba(249,249,249,0.65));
  backdrop-filter: blur(12px);
  border-radius: 16px;
  box-shadow: 0 4px 25px rgba(0, 0, 0, 0.08);
  overflow: hidden;
}

.panel-title {
  font-size: 1.4rem;
  font-weight: bold;
  color: white;
  background: linear-gradient(135deg, var(--orange), var(--orange-hover));
  text-align: center;
  padding: 0.8rem 1rem;
  border-bottom: 2px solid rgba(255, 255, 255, 0.2);
  position: sticky;
  top: 0;
  z-index: 2;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.scroll-container {
  flex: 1;
  overflow-y: auto;
  padding: 1rem;
  gap: 14px;
  display: flex;
  flex-direction: column;
}

.scroll-container::-webkit-scrollbar {
  width: 8px;
}
.scroll-container::-webkit-scrollbar-thumb {
  background-color: var(--orange);
  border-radius: 4px;
}
.scroll-container::-webkit-scrollbar-track {
  background-color: transparent;
}

.comic-card {
  background: white;
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0,0,0,0.08);
  overflow: hidden;
  cursor: pointer;
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}
.comic-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 6px 16px rgba(0,0,0,0.15);
}

.comic-thumbnail {
  width: 100%;
  height: 420px;
  object-fit: cover;
  display: block;
}

.comic-name {
  padding: 0.5rem;
  font-weight: 600;
  font-size: 0.95rem;
  color: #333;
  text-align: center;
  background: #fafafa;
}

@media (max-width: 768px) {
  .comic-thumbnail {
    height: 300px;
  }
}
</style>
