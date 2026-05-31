<script setup>
import {
  LayoutDashboard,
  Compass,
  MessageSquare,
  LogOut
} from 'lucide-vue-next'

import { RouterLink } from 'vue-router'
import { useUserStore } from '@/stores/user'

const userStore = useUserStore()
</script>

<template>

<div class="sidebar">

  <h1 class="logo">Synaptix</h1>

  <RouterLink to="/" class="nav-item">
    <LayoutDashboard :size="20" />
    Board
  </RouterLink>

  <RouterLink to="/explore" class="nav-item">
    <Compass :size="20" />
    Find
  </RouterLink>

  <RouterLink to="/chat/14" class="nav-item">
    <MessageSquare :size="20" />
    Chats
  </RouterLink>

  <button
    class="logout-btn"
    @click="userStore.logout()"
  >
    <LogOut :size="20" />
    Leave
  </button>

</div>

</template>

<style scoped>
.sidebar {
  width: 500px;
  height: 100vh;
  background: #0b1120;
  border-right: 1px solid rgba(255,255,255,0.08);
  position: fixed;
  left: 0;
  top: 0;
  padding: 2rem 1rem;
  display: flex;
  flex-direction: column;
  gap: 1rem;
}
button:hover {
  cursor: pointer;
}

.logo {
  color: white;
  margin-bottom: 2rem;
}

.nav-item,
.logout-btn {
  display: flex;
  align-items: center;
  gap: 0.8rem;
  padding: 1rem;
  border-radius: 12px;
  color: white;
  text-decoration: none;
  background: rgba(255,255,255,0.03);
  border: none;
  cursor: pointer;
}

.nav-item:hover {
  background: rgba(59,130,246,0.2);
}
</style>