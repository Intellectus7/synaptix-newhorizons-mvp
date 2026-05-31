<script setup>
import { ref } from 'vue'
import { useApiStore } from '@/stores/api'
import { useRouter } from 'vue-router'

const router = useRouter()

function chatWithBot() {
  router.push(
    `/chat/${createdBotId.value}`
  )
}
const apiStore = useApiStore()

const botName = ref('')
const systemPrompt = ref('')

const loading = ref(false)
const error = ref('')
const createdBotId = ref(null)

async function createBot() {
  error.value = ''

  if (!botName.value.trim()) {
    error.value = 'Bot name is required'
    return
  }

  if (!systemPrompt.value.trim()) {
    error.value = 'System prompt is required'
    return
  }

  loading.value = true

  try {
    const response = await apiStore.post(
      '/bots/create',
      {
        name: botName.value,
        system_prompt: systemPrompt.value
      }
    )

    createdBotId.value =
      response.data.bot_id

  } catch (err) {
    error.value =
      err?.response?.data?.message ||
      'Failed to create bot'
  }

  loading.value = false
}

</script>

<template>
  <div class="container">

    <h1>Create Bot</h1>

    <template v-if="!createdBotId">

      <input
        v-model="botName"
        class="input"
        placeholder="Bot Name"
      />

      <textarea
        v-model="systemPrompt"
        class="textarea"
        placeholder="You are a physics teacher..."
      />

      <button
        @click="createBot"
        :disabled="loading"
        class="button"
      >
        {{ loading ? 'Creating...' : 'Create Bot' }}
      </button>

      <p
        v-if="error"
        class="error"
      >
        {{ error }}
      </p>

    </template>

    <template v-else>

      <h2>Bot Created 🎉</h2>

      <p>
        Share this Bot ID:
      </p>

      <div class="bot-id">
        {{ createdBotId }}
      </div>

      <p>
        Other users can search
        for this ID and start
        chatting with your bot.
      </p>
    <button
        @click="chatWithBot"
    >
        Open Chat
    </button>

    </template>

  </div>
</template>

<style scoped>
.container {
  max-width: 700px;
  margin: auto;
  padding: 2rem;
}

.input,
.textarea {
  width: 100%;
  margin-bottom: 1rem;
  padding: 1rem;
  border-radius: 8px;
}

.textarea {
  min-height: 250px;
  resize: vertical;
}

.button {
  padding: 1rem;
}

.error {
  color: red;
  margin-top: 1rem;
}

.bot-id {
  font-size: 2rem;
  font-weight: bold;
  margin: 1rem 0;
}
button:hover {
    cursor: pointer;
}
</style>