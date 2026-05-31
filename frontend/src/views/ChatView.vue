<script setup>
import { useRoute } from 'vue-router'
import { useApiStore } from '@/stores/api'
import { useUserStore, useBaseUrl } from '@/stores/user'
import { ref, onMounted, onUnmounted, nextTick } from 'vue'
import { io } from 'socket.io-client'

const route = useRoute()
const apiStore = useApiStore()
const userStore = useUserStore()
const baseUrl = useBaseUrl()
const nexusId = ref(14);
const userId = Number(route.params.userId)
const myId = ref('');
const username = ref('Loading...')
const messages = ref([])
const newMessageText = ref('')
const messagesBox = ref(null)

let socket = null

const formatTime = (isoString) => {
  if (!isoString) return ''

  return new Date(isoString).toLocaleTimeString([], {
    hour: '2-digit',
    minute: '2-digit'
  })
}

const scrollToBottom = async () => {
  await nextTick()

  if (messagesBox.value) {
    messagesBox.value.scrollTop =
      messagesBox.value.scrollHeight
  }
}

async function answerQuestionInChat(question, context) {
    const body = {
        question: question,
        context: context
    }
    const response = await apiStore.post('/nexus/answerQuestion', body);
    socket.emit('send_msg', {
    receiver_id: myId.value,
    content: response.data
  })

}
onMounted(async () => {
  try {
    const BASE_URL = baseUrl.getBaseUrl()
    const profile = await userStore.fetchProfile();
    myId.value = profile.id;
    // Load user + history
    const response = await apiStore.get(
      `/users/getUserInfo?userId=${userId}`
    )

    username.value = response.data.the_user.username

    messages.value =
      response.data.correspondence.map(msg => ({
        ...msg,
        is_me:
          msg.sender_id === myId.value
      }))

    await scrollToBottom()

    // Connect socket
    socket = io(BASE_URL, {
      auth: {
        token: localStorage.getItem('session_key')
      }
    })

    socket.on('connect', () => {
      console.log('CONNECTED')

      socket.emit('join_chat', {
        target_id: userId
      })
    if ( userId === nexusId.value) {
        newMessageText.value = localStorage.getItem('nexusQuery', 'Describe Synaptix');
        const query = newMessageText.value;
        sendChat();
//      answerQuestionInChat(query, messages.value);
    }
    })

    socket.on('connect_error', (err) => {
      console.error(
        'SOCKET ERROR:',
        err
      )
    })



    socket.on('disconnect', (reason) => {
      console.log(
        'DISCONNECTED:',
        reason
      )
    })

    socket.on('receive_msg', async (msg) => {
      console.log(
        'RECEIVED:',
        msg
      )

      msg.is_me =
        msg.sender_id === myId.value;

      // Ignore duplicate optimistic message
      let exists = messages.value.some(
        m =>
          m.id === msg.id
      )
      if (localStorage.getItem('lastMsg') === msg) {
        exists = true
      }

      if (!exists) {
        messages.value.push(msg)
        localStorage.setItem('lastMsg', msg);
        await scrollToBottom()
      }
    })

  } catch (err) {
    console.error(
      'Chat interface runtime error:',
      err
    )
  }
})

onUnmounted(() => {
  if (socket) {
    socket.off('connect')
    socket.off('connect_error')
    socket.off('disconnect')
    socket.off('receive_msg')

    socket.disconnect()
  }
})

const sendChat = async () => {

  const content =
    newMessageText.value.trim()

  if (!content) return

  if (!socket?.connected) {
    alert("NOT CONNECTED")
    console.error(
      'Socket not connected'
    )
    return
  }

  // Optimistic message
  const tempMessage = {
    id: `temp-${Date.now()}`,
    sender_id: userStore.user.id,
    receiver_id: userId,
    content,
    timestamp: new Date().toISOString(),
    is_me: true
  }

//    messages.value.push(tempMessage)

  await scrollToBottom()

  socket.emit('send_msg', {
    receiver_id: userId,
    content
  })

  newMessageText.value = ''
}
</script>

<template>
  <div class="chat-container">
    <h1>Chat with {{ username }}</h1>
    
    <div ref="messagesBox" class="messages-box">
      <div v-for="msg in messages" :key="msg.id" class="bubble-wrapper" :class="{ 'sent-wrapper': msg.is_me }">
        <div class="bubble" :class="{ 'sent': msg.is_me, 'received': !msg.is_me }">
          <p class="text">{{ msg.content }}</p>
        </div>
        <span class="time-stamp">{{ formatTime(msg.timestamp) }}</span>
      </div>
    </div>
    
    <input 
      v-model="newMessageText" 
      @keydown.enter.prevent="sendChat"
      type="text" 
      class="input" 
      placeholder="Type a message and hit enter..." 
    />
  </div>
</template>

<style scoped>
.chat-container {
  display: flex;
  flex-direction: column;
  height: 85vh;
  padding: 1rem;
}

.messages-box {
  flex-grow: 1;
  overflow-y: auto;
  display: flex;
  flex-direction: column;
  gap: 1rem;
  padding: 1rem;
  background: rgba(255,255,255,0.02);
  border-radius: 8px;
}

.bubble-wrapper {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  max-width: 60%;
}

.sent-wrapper {
  align-self: flex-end;
  align-items: flex-end;
}

.bubble {
  padding: 0.75rem 1rem;
  border-radius: 16px;
  color: white;
}

.sent {
  background: #2563eb;
  border-bottom-right-radius: 4px;
}

.received {
  background: #334155;
  border-bottom-left-radius: 4px;
}

.time-stamp {
  font-size: 0.7rem;
  color: #64748b;
  margin-top: 0.25rem;
  padding: 0 0.25rem;
}

.input {
  margin-top: 1rem;
  padding: 1rem;
  border-radius: 8px;
  border: none;
  background: rgba(255,255,255,0.05);
  color: white;
}
</style>
