<script setup>
import { RouterView } from 'vue-router'
import { ref } from 'vue'

const isMenuOpen = ref(false)

const toggleMenu = () => {
  isMenuOpen.value = !isMenuOpen.value
}
</script>

<template>
  <!-- Top Navigation Bar -->
  <header class="topbar">
    <div class="logo">My App</div>

    <!-- Hamburger (mobile only) -->
    <button class="hamburger" @click="toggleMenu" aria-label="Toggle Menu">
      ☰
    </button>

    <!-- Nav Links -->
    <nav :class="{ open: isMenuOpen }">
      <router-link to="/" active-class="active">Intro</router-link>
      <router-link to="/info" active-class="active">The Visual Impaired</router-link>
      <router-link to="/gn-diff" active-class="active">Types of Graphic Novels</router-link>
      <router-link to="/parts" active-class="active">Parts of Comics</router-link>
      <router-link to="/challenges" active-class="active">Challenges</router-link>
      <router-link to="/ml" active-class="active">Machine Learning</router-link>
      <router-link to="/dl" active-class="active">Deep Learning</router-link>
    </nav>
  </header>

  <!-- Main Content -->
  <main class="main-content">
    <RouterView />
  </main>
</template>

<style>
html, body {
  margin: 0;
  padding: 0;
  height: 100%;
  width: 100%;
}

#app{
  max-width:100%;
}

/* ===== TOP BAR ===== */
.topbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background-color: #da7434;
  padding: 0.5rem 1rem;
  position: sticky;
  top: 0;
  z-index: 1000;
}

.logo {
  font-size: 1.2rem;
  font-weight: bold;
  color: white;
}

.topbar nav {
  display: flex;
  gap: 1rem;
}

.topbar nav a {
  color: white;
  text-decoration: none;
  font-weight: bold;
  padding: 0.5rem;
  transition: color 0.3s ease;
}

.topbar nav a:hover,
.topbar nav a.active {
  color: #00bfff;
}

.hamburger {
  display: none;
  font-size: 1.5rem;
  background: transparent;
  border: none;
  color: white;
  cursor: pointer;
}

/* ===== MOBILE MENU ===== */
@media (max-width: 768px) {
  .hamburger {
    display: block;
  }

  .topbar nav {
    display: none;
    flex-direction: column;
    position: absolute;
    top: 100%;
    right: 0;
    background-color: #da7434;
    width: 200px;
    padding: 0.5rem 0;
  }

  .topbar nav.open {
    display: flex;
  }

  .topbar nav a {
    padding: 0.7rem 1rem;
  }
}

/* ===== FULLSCREEN MAIN CONTENT ===== */
.main-content {
  padding: 0; /* Remove padding so content takes full width */
  height: calc(100vh - 50px); /* Full height minus header */
  width: 100%; /* Take full width */
  overflow-y: auto;
}
</style>
