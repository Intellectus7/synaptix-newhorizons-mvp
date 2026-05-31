<script setup>
import DashboardHero from './DashBoardHero.vue'
import Sidebar from './Sidebar.vue';
</script>


<template>
  <main>
    <Sidebar class="cyber-panel max-w-32 h-screen no-border-radius"/>
    <DashboardHero class="imp"/>
  </main>
</template>

<style scoped>
  .no-border-radius {
    border-radius: 0px;
    z-index: 100;
  }
.imp {
  z-index: 10;
}
</style>