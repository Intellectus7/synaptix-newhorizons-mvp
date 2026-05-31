<script setup>
import { ref, watch } from 'vue'
import Sidebar from '@/components/Sidebar.vue'
import SearchBar from '@/components/SearchBar.vue'
import UserCard from '@/components/UserCard.vue'
import { useApiStore } from '@/stores/api'

const apiStore = useApiStore()

const search = ref('')
const users = ref([])
const search_results = ref([])

watch(search, async () => {

  if (!search.value) {
    users.value = []
    return
  }

  try {

    const response = await apiStore.get(
      `/users/search?query=${search.value}`
    )

    users.value = response
    search_results.value = response
    console.log('Logging users');
  } catch (err) {
    console.error(err)
  }
})
</script>

<template>

<div class="layout">

  <Sidebar class="max-w-64"/>

  <main class="main">
    {{ search_results.data || 'No search results' }}
    <SearchBar v-model="search" />

    <div class="results">

      <UserCard
        v-for="user in users.data"
        :key="user.id"
        :user="user"
      />

    </div>

  </main>

</div>

</template>

<style scoped>
.layout {
  display: flex;
  min-height: 100vh;
  background: #020617;
}

.main {
  margin-left: 250px;
  width: 100%;
  padding: 2rem;
}

.results {
  margin-top: 2rem;
  display: flex;
  flex-direction: column;
  gap: 1rem;
}
</style>