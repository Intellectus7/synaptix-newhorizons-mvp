<script setup>
import { RouterLink } from 'vue-router'

</script>

<template>
  <div class="flex flex-col justify-center hero items-center glass-card">
    <h1 class="hero-title justify-center relative"> Welcome to Synaptix </h1>
    <p class="hero-subtitle"> Make your AI dreams come true in minutes</p>
    <p class="hero-subtitle">Confused? See our <RouterLink to="/about"> About page </RouterLink></p>
    <button class="btn-primary"><RouterLink to="/register"> Register now</RouterLink></button>
  </div>
</template>


<style scoped>

</style>