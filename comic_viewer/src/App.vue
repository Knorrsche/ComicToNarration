<script setup>
import { RouterView } from 'vue-router'
import { ref, onMounted, onUnmounted } from 'vue'

const currentSection = ref('header')
const isSidebarOpen = ref(false)

const toggleSidebar = () => {
  isSidebarOpen.value = !isSidebarOpen.value
}

const handleClickOutside = (event) => {
  if (!event.target.closest('.sidebar') && !event.target.closest('.hamburger')) {
    isSidebarOpen.value = false
  }
}

onMounted(() => {
  document.addEventListener('click', handleClickOutside)
})

onUnmounted(() => {
  document.removeEventListener('click', handleClickOutside)
})
</script>

<template>
  <button class="hamburger" @click="toggleSidebar">
    ☰
  </button>

<nav class="sidebar" :class="{ open: isSidebarOpen }">
  <ul>
    <li><router-link to="/" active-class="active">Intro</router-link></li>
    <li><router-link to="/info" active-class="active">The Visual Impaired</router-link></li>
    <li><router-link to="/gn-diff" active-class="active">Types of Graphic Novels</router-link></li>
    <li><router-link to="/parts" active-class="active">Parts of Comics</router-link></li>
    <li><router-link to="/challenges" active-class="active">Challenges</router-link></li>
    <li><router-link to="/ml" active-class="active">Machine Learning</router-link></li>
    <li><router-link to="/dl" active-class="active">Deep Learning</router-link></li>
  </ul>
</nav>

  <RouterView />
</template>
.router-view-wrapper {
  height: 100vh; /* forces it to exactly match viewport height */
}
<style>
html, body {
  margin: 0;
  padding: 0;
  height: 100%;
  width: 100%;
}

app {
  height: 100%;
  display: flex;
}

.sidebar {
  position: fixed;
  top: 0;
  left: 0;
  height: 100vh;
  width: clamp(150px, 18vw, 250px);
  background-color: #da7434;
  padding-top: 2rem;
  z-index: 1000;
  transition: transform 0.3s ease, width 0.3s ease;
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
  color: white;
  text-decoration: none;
  font-weight: bold;
  transition: color 0.3s ease;
  display: block;
  padding: 0.5rem 0;
}

.sidebar a:hover,
.sidebar a.active {
  color: #00bfff;
}

.sidebar li:has(a.active)::before {
  content: '';
  position: absolute;
  left: 0;
  top: 0;
  height: 100%;
  width: 6px;
  background-color: #00bfff;
  border-radius: 3px;
}

.hamburger {
  display: none;
  position: fixed;
  top: 15px;
  left: 15px;
  font-size: 2rem;
  background: transparent;
  border: none;
  color: white;
  z-index: 1100;
  cursor: pointer;
}

@media (max-width: 768px) {
  .hamburger {
    display: block;
    background: #007bff;
  }

  .sidebar {
    transform: translateX(-100%);
    width: 250px;
    height: 100vh;
    padding-top: 2rem;
  }

  .sidebar.open {
    transform: translateX(0);
  }
}
</style>
