<script setup>
import TheWelcome from '../components/TheWelcome.vue'
import HelloWorld from '@/components/HelloWorld.vue';
import { useUserStore } from '@/stores/user';
import { ref } from 'vue'

const userStore = useUserStore();
const isUser = ref(localStorage.getItem('session_key') || null);
</script>

<template>
  <main v-if="isUser">
    <HelloWorld />
  </main>  
  <main v-else> 
    <TheWelcome />
  </main>
</template>
