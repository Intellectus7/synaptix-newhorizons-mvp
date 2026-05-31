<script setup>
import { RouterLink, useRouter } from 'vue-router'
import { ref, onMounted } from 'vue'
import { useUserStore } from '@/stores/user'
import { useApiStore } from '@/stores/api'
import {
  Plus,
  Sparkles,
  MessageCircle,
  ArrowRight
} from 'lucide-vue-next'

const router = useRouter();
const userStore = useUserStore()
const username = ref('');
const id = ref('');
const query = ref('');
const apiStore = useApiStore();
const nexusId = ref(0);

function NeuronChat() {
  localStorage.setItem('nexusQuery', query.value);
  router.push(`/chat/${nexusId.value}`);
}
onMounted(async() => {
  const profile = await userStore.fetchProfile();
  const nexusResponse = await apiStore.get('/getnexusid')
  nexusId.value = Number(nexusResponse.data.id)
  console.log('Fetch profile response', profile);
  if (profile) {
    console.log("Profile")
    username.value = profile.username;
    id.value = profile.id;
  } else {
  console.log("No profile")
    username.value = 'User';
    id.value = '...';
  }
});
</script>

<template>

<div class="hero">

  <div>
    <h1>
      Welcome back,
      {{ username }}
    </h1>

    <p>
      User ID:
      #{{ id }}
    </p>
  </div>
  <div class="chat chat-container bot-card">
    <form action="" @submit.prevent="NeuronChat">
      <input type="text" class="input" placeholder="Ask anything (preferably about Synaptix)" v-model="query" @keydown.enter="NeuronChat" />
      <button type="submit" class="ai-btn absolute"><ArrowRight :size="20"/></button>
    </form>
  </div>
  <div class="actions">
  
    <button class="hero-btn">
      <Plus :size="18" />
        <RouterLink to="/bot">
          Create Bot
        </RouterLink>
      
    </button>

    <button class="hero-btn">
      <MessageCircle :size="18" />
        <RouterLink to="/chat">
          Start Chat
        </RouterLink>
    </button>

    <button class="hero-btn">
      <Sparkles :size="18" />
        <RouterLink to="/explore">
          Explore
        </RouterLink>
    </button>

  </div>

</div>

</template>

<style scoped>
.actions {
  display: flex;
  gap: 1rem;
}


.hero-btn {
  display: flex;
  align-items: center;
  gap: 0.5rem;

  background: rgba(255,255,255,0.08);
  border: none;
  color: white;

  padding: 0.9rem 1.2rem;
  border-radius: 12px;

  cursor: pointer;
}

.hero {
  background: linear-gradient(
    135deg,
    rgba(59,130,246,0.15),
    rgba(147,51,234,0.12)
  );

  border: 1px solid rgba(255,255,255,0.08);

  padding: 2rem;
  border-radius: 24px;

  display: flex;
  justify-content: space-between;
  align-items: center;

  color: white;
}
.stats {
  border-radius: 10px;
  padding: 20px;
  background-color: black;
  height: 50px;
  width: 50px;
}
.chat {
  width: 75vw;
  height: 30vh;
  border-radius: 10px;
  left: 5vw;
}
.ai-btn {
  width: 2.5vw;
  height: 2.5vw;
  background-color: aquamarine;
  border-radius: 50%;
}
.ai-btn:hover {
  cursor: pointer;
}
</style>