<script setup>
import { RouterView } from 'vue-router'
</script>

<template>
   <nav class="sidebar">
      <ul>
        <li><a :class="{ active: currentSection === 'header' }" href="/#header">Intro</a></li>
        <li><a :class="{ active: currentSection === 'info' }" href="/#info">The Visual Impaired</a></li>
        <li><a :class="{ active: currentSection === 'gn-diff' }" href="/#gn-diff">Types of Graphic Novels</a></li>
        <li><a :class="{ active: currentSection === 'parts' }" href="/#parts">Parts of Comics</a></li>
        <li><a :class="{ active: currentSection === 'challenges' }" href="/#challenges">Challenges</a></li>
        <li><a :class="{ active: currentSection === 'segment' }" href="/ml">Machine Learning</a></li>
        <li><a :class="{ active: currentSection === 'bounding' }" href="/dl">Deep Learning</a></li>
      </ul>
    </nav>
  <RouterView />
</template>

<style>
body, html {
  margin: 0;
  padding: 0;
  height: 100%;
}
#app {
  height: 100%;
}
.sidebar {
  position: fixed;
  top: 0;
  left: 0;
  height: 100vh;
  width: 200px;
  background-color: #da7434;
  padding-top: 30px;
  z-index: 1000;
}

.sidebar ul {
  list-style: none;
  padding: 0;
  margin: 0;
}

.sidebar li {
  margin: 20px 0;
  text-align: center;
  position: relative;
}

.sidebar a {
  color: white;
  text-decoration: none;
  font-weight: bold;
  transition: color 0.3s ease;
  display: block;
  padding: 10px 0;
  position: relative;
  z-index: 1;
}

.sidebar a:hover {
  color: #00bfff;
}

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

</style>

