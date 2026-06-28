<script setup>
    import SidebarCard from '../components/SidebarCard.vue'
    import { MessageCircle } from 'lucide-vue-next'
    import { useRouter } from 'vue-router'
    import { useApiStore } from '@/stores/api'
    import { onMounted, ref } from 'vue'

    const apiStore = useApiStore();
    const data = ref([]);
    onMounted(async() => {
        const res = await apiStore.get('/getSidebarInfo');
        data.value = res.conversations || res.data.conversations;
    })
</script>

<template>
  <div class="header">
      <h1>Messages</h1>
  
      <p>
          Continue conversations with people and AI.
      </p>
  </div>
    <div class="container h-full w-full">
        <div v-for="item in data" :key="item.other_user">
            <SidebarCard :userId="item.other_user" :isBot="item.is_ai" :lastMsg="item.last_message" :avatar="item.profile_pic" :username="item.username" class="conversation"/>
        </div>
    </div>
  <div
      v-if="!data.length"
      class="empty"
  >
      <MessageCircle :size="56" />
  
      <h2>No conversations yet</h2>
  
      <p>
          Start chatting with someone or an AI.
      </p>
  </div>
</template>

<style scoped>
  .container{
    max-width:850px;

    margin:auto;

    padding:2rem 1rem;

    display:flex;
    flex-direction:column;

    gap:1rem;
}
.header{
    margin-bottom:1rem;
}

.header h1{
    color:white;

    font-size:2rem;

    margin:0;
}

.header p{
    color:#9d9d9d;

    margin-top:.35rem;
}
.conversation{

    animation:fadeUp .25s ease;

}

@keyframes fadeUp{

from{

opacity:0;

transform:translateY(10px);

}

to{

opacity:1;

transform:translateY(0);

}

}

.container{

width:min(900px,100%);

}
.container {
  gap: 1rem;
.conversation {
  width: 100%;

</style>
