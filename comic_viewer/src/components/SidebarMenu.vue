<script setup>
import { ref, onMounted, onBeforeUnmount } from 'vue'

const props = defineProps({
  sections: {
    type: Array,
    required: true
  }
})

const isMenuOpen = ref(window.innerWidth >= 1024)
const activeSection = ref('')
let scrollContainer = null

const toggleMenu = () => {
  isMenuOpen.value = !isMenuOpen.value
}

const handleScroll = () => {
  if (!scrollContainer) return

  const scrollPos = scrollContainer.scrollTop + 160
  let current = props.sections[0]?.id || ''

  props.sections.forEach(section => {
    const el = document.getElementById(section.id)
    if (el && el.offsetTop <= scrollPos) {
      current = section.id
    }
  })

  activeSection.value = current
}

onMounted(() => {
  scrollContainer = document.querySelector('.scroll-container')
  if (scrollContainer) {
    scrollContainer.addEventListener('scroll', handleScroll, { passive: true })
    handleScroll()
  }
})

onBeforeUnmount(() => {
  if (scrollContainer) {
    scrollContainer.removeEventListener('scroll', handleScroll)
  }
})
</script>

<template>
  <!-- Hamburger -->
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
      <li
        v-for="section in sections"
        :key="section.id"
        :class="{ active: activeSection === section.id }"
      >
        <a :href="'#' + section.id" @click="isMenuOpen = window.innerWidth >= 1024 ? true : false">
          {{ section.title }}
        </a>
      </li>
    </ul>
  </nav>
</template>

<style scoped>
/* Colors */
:global(:root) {
  --orange-primary: #da7434;
  --orange-light: #ffb68a;
}

/* Hamburger */
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
  background-color: var(--orange-primary);
  border: 3px solid white;
  border-radius: 8px;
  padding: 8px;
  cursor: pointer;
  transition: transform 0.2s ease, border-color 0.3s ease;
}

.hamburger:hover {
  transform: scale(1.05);
  border-color: var(--orange-light);
}

.hamburger span {
  display: block;
  height: 3px;
  background: white;
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
  background-color: rgba(218, 116, 52, 0.95);
  backdrop-filter: blur(8px);
  border-radius: 0 12px 12px 0;
  box-shadow: 4px 0 20px rgba(0, 0, 0, 0.15);
  padding-top: 4rem;
  z-index: 1500;
  transition: left 0.35s ease, opacity 0.35s ease;
  opacity: 0;
}

.sidebar.open {
  left: 0;
  opacity: 1;
}

.sidebar ul {
  list-style: none;
  padding: 0;
  margin: 0;
}

.sidebar li {
  margin: 1.5rem 0;
  text-align: center;
}

.sidebar a {
  color: #fff;
  text-decoration: none;
  font-weight: 600;
  font-size: 1.25rem;
  transition: all 0.3s ease;
}

.sidebar li.active a {
  background: white;
  color: var(--orange-primary);
  padding: 0.5rem 1rem;
  border-radius: 8px;
  box-shadow: 0 0 10px rgba(255, 255, 255, 0.4);
}

.sidebar a:hover {
  color: #ffe9dc;
}
</style>
