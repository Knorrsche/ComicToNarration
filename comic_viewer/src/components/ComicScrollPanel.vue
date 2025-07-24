<script setup>
import { useRouter } from 'vue-router';
import {nextTick, onMounted, ref} from "vue";

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
    loading.value = true;
    const response = await fetch(
      `http://localhost:8000/comic-page?comic=${encodeURIComponent(comicName)}&page=${encodeURIComponent(pageFilename)}`
    );
    if (!response.ok) throw new Error("Failed to load comic page");

    const data = await response.json();
    imageSrc.value = `data:${data.mimeType};base64,${data.image}`;

    const parser = new DOMParser();
    const xmlDoc = parser.parseFromString(data.annotations, "application/xml");
    boundingBoxes.value = extractBoxesFromXml(xmlDoc);

    await nextTick();
    updateScale();
  } catch (err) {
    console.error("Error loading page:", err);
  } finally {
    loading.value = false;
  }
};

onMounted(async () => {
  try {
    const res = await fetch("http://localhost:8000/comics");
    if (!res.ok) throw new Error("Failed to fetch comics");
    const comics = await res.json();
    comicList.value = comics;
  } catch (err) {
    console.error("Error loading comic list:", err);
  }

  window.addEventListener("resize", updateScale);
});

</script>

<template>
<div class="comic-scroll-panel">
  <h3>Select a Comic</h3>
  <div class="scroll-container">
  <div
    v-for="(comic, index) in comicList"
    :key="index"
    class="comic-item-with-preview"
    @click="goToViewer(comic.name)"
  >
<img :src="`http://localhost:8000/comics/${comic.name}/${comic.pages[0]}`"
     alt="preview"
     class="comic-thumbnail" />
    </div>
  </div>
</div>
</template>

<style scoped>
.scroll-container {
  display: flex;
  flex-direction: column;
  overflow-y: auto;
  overflow-x: hidden;
  max-height: 65vh;
  width:350px;
  gap: 12px;
  padding-right: 4px;
}

.comic-item-with-preview {
  flex: 0 0 auto;
  width: 100px;
  text-align: center;
  cursor: pointer;
}

.comic-thumbnail {
  width: 300px;
  height: 420px;
  object-fit: cover;
  border-radius: 4px;
  box-shadow: 0 0 4px rgba(0, 0, 0, 0.2);
  margin-bottom: 6px;
}

.comic-name {
  font-weight: 600;
  font-size: 0.8rem;
  color: #333;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}
</style>