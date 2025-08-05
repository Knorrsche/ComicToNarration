<script setup>
import { ref } from 'vue'

// Props: sections array
const props = defineProps({
  sections: {
    type: Array,
    required: true
  }
})

const isMenuOpen = ref(false)
const toggleMenu = () => {
  isMenuOpen.value = !isMenuOpen.value
}
</script>

<template>
  <!-- Modern Orange Hamburger -->
  <button
    class="hamburger"
    :class="{ open: isMenuOpen }"
    @click="toggleMenu"
    aria-label="Toggle Menu"
  >
    <span></span>
    <span></span>
    <span></span>
  </button>

  <!-- Sidebar -->
  <nav class="sidebar" :class="{ open: isMenuOpen }">
    <ul>
      <li v-for="section in sections" :key="section.id">
        <a :href="'#' + section.id" @click="isMenuOpen = false">
          {{ section.title }}
        </a>
      </li>
    </ul>
  </nav>
</template>

<style scoped>
:root {
  --orange-primary: #da7434;
  --orange-light: #ffe9dc;
}

/* Hamburger Button */
.hamburger {
  position: fixed;
  top: 1rem;
  left: 1rem;
  z-index: 9999;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  width: 40px;
  height: 40px;
  background: white;
  border: 2px solid var(--orange-primary);
  border-radius: 8px;
  padding: 8px;
  cursor: pointer;
  transition: all 0.2s ease;
}

.hamburger:hover {
  background: var(--orange-light);
  transform: scale(1.05);
}

.hamburger span {
  display: block;
  height: 3px;
  background: var(--orange-primary);
  border-radius: 2px;
  transition: 0.3s ease;
}

.hamburger.open span:nth-child(1) {
  transform: translateY(8px) rotate(45deg);
}
.hamburger.open span:nth-child(2) {
  opacity: 0;
}
.hamburger.open span:nth-child(3) {
  transform: translateY(-8px) rotate(-45deg);
}

/* Sidebar */
.sidebar {
  position: fixed;
  top: 0;
  left: -260px;
  height: 100vh;
  width: 250px;
  background: var(--orange-primary);
  box-shadow: 2px 0 8px rgba(0,0,0,0.15);
  padding-top: 4rem;
  z-index: 1500;
  transition: left 0.3s ease;
}

.sidebar.open {
  left: 0;
}

.sidebar ul {
  list-style: none;
  padding: 0;
  margin: 0;
}

.sidebar li {
  margin: 1.2rem 0;
  text-align: center;
}

.sidebar a {
  color: #fff;
  text-decoration: none;
  font-weight: 500;
  font-size: 1rem;
  transition: all 0.3s ease;
}

.sidebar a:hover,
.sidebar a.active {
  color: #ffe9dc;
  text-shadow: 0 0 6px rgba(255, 255, 255, 0.4);
}
</style>
