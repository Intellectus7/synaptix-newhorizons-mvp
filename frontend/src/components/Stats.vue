<script setup>
import { useUserStore } from '@/stores/user';
import { ref, onMounted } from 'vue'

const userStore = useUserStore();
const profile = ref({});

onMounted(async() => {
    profile.value = await userStore.fetchProfile();
})
</script>

<template>
    <div class="container">
        Your Acheivements
        {{ profile.messages }}
    </div>
</template>

<style scoped></style>