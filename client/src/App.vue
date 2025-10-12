<script setup>
  import Navbar from "@/components/navbar/Navbar.vue"
</script>

<template>
  <Navbar/>
  <router-view />
</template>

<style>
/* 1. Use a more-intuitive box-sizing model */
*,
*::before,
*::after {
  box-sizing: border-box;
  font-family: inherit;
}

/* 2. Remove default margin */
* {
  margin: 0;
}

/* 3. Enable keyword animations */
@media (prefers-reduced-motion: no-preference) {
  html {
    interpolate-size: allow-keywords;
  }
}

html {
  width: 100%;
  height: auto;
  overflow-x: hidden;
}

body,
#app {
  /* 4. Add accessible line-height */
  line-height: 1.5;
  /* 5. Improve text rendering */
  -webkit-font-smoothing: antialiased;
  min-height: 100vh;
  min-width: 100vw;
  font-family: 'Manrope', 'sans-serif';
  overflow-x: hidden;
}

/* 6. Improve media defaults */
img,
picture,
video,
canvas,
svg {
  display: block;
  max-width: 100%;
}

/* 7. Inherit fonts for form controls */
input,
button,
textarea,
select {
  font: inherit;
}

/* 8. Avoid text overflows */
p,
h1,
h2,
h3,
h4,
h5,
h6 {
  overflow-wrap: break-word;
}

/* 9. Improve line wrapping */
p {
  text-wrap: pretty;
}
h1,
h2,
h3,
h4,
h5,
h6 {
  text-wrap: balance;
}
.font-display {
  font-family: "Bungee", 'sans-serif';
  font-weight: 400;
}
.font-mali {
    font-family: "Mali", cursive;
  font-weight: 400;
  font-style: normal;
}
</style>
