<script setup>
import { RouterLink, RouterView } from 'vue-router'
import { ref } from 'vue'

//localStorage.clear();
const user = ref(localStorage.getItem('session_key'));
</script>

<template>
  <header>
    <nav class="navbar important">
          <RouterLink to="/">Home</RouterLink>
          <RouterLink to="/about">About</RouterLink>
          <RouterLink to="/register" v-if="!user">Sign Up</RouterLink>
          <RouterLink to="/login" v-if="!user">Log In</RouterLink>
    </nav>
  </header>
  <RouterView />
</template>


<style scoped>
  .important {
    z-index: 1000;
  }
</style>
