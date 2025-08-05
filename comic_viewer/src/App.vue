<template>
  <router-view />
</template>

<script setup>
</script>

<style>
* {
  box-sizing: border-box;
}

html, body {
  margin: 0;
  padding: 0;
  height: 100%;
  scroll-behavior: smooth;
  font-family: "Inter", "Segoe UI", Roboto, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  background-color: #fafafa;
  color: #222;
}

a {
  text-decoration: none;
  color: inherit;
}

ul {
  margin: 0;
  padding: 0;
  list-style: none;
}
</style>
