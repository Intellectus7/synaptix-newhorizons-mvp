<script setup>
import { MessageCircle } from 'lucide-vue-next'
import { useRouter } from 'vue-router'
import { useUserStore } from '@/stores/user'

const userStore = useUserStore();

const props = defineProps({
  user: Object
})

const router = useRouter()

async function addContact(user_id) {
  await userStore.addContact(user_id);
  console.log("Adding user contact");

}
function messageUser() {
  router.push(`/chat/${props.user.id}`)
}
</script>

<template>

<div class="card">
  
  <div v-if="user">
    This is a user
    <h2>{{ user.username }}</h2>
    <p>#{{ user.id }}</p>
  </div>
  <div v-else>
    We can't find a user with that id.
    <p>Try checking the id</p>
  </div>

  <button
    class="message-btn"
    @click="messageUser"
  >
    <MessageCircle :size="18" />
    Message
  </button>

</div>

</template>

<style scoped>
.card {
  background: rgba(255,255,255,0.04);
  border: 1px solid rgba(255,255,255,0.06);
  border-radius: 18px;
  padding: 1.2rem;

  display: flex;
  justify-content: space-between;
  align-items: center;

  color: white;
}

.message-btn {
  display: flex;
  align-items: center;
  gap: 0.5rem;

  border: none;
  border-radius: 12px;
  padding: 0.8rem 1rem;

  background: #2563eb;
  color: white;

  cursor: pointer;
}
</style>