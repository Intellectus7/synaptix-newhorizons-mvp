import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'

const BASE_URL = 'http://localhost:5000'
const router = useRouter();
const contactList = ref([]);

export const useBaseUrl = defineStore('base', () => {
  function getBaseUrl() {
    return BASE_URL;
  }
  return { getBaseUrl }
})

export const useContactList = defineStore('contact', () => {
  function getContacts() {
    return contactList;
  }
  async function getUserCredentials(user_id) {
    const route = `/users/getUserInfo?userId=${user_id}`;
    const config = {
      method: 'GET',
      headers: {'Content-Type': 'application/json'},
      credentials: 'include'
    }
    const response = await fetch(`${BASE_URL}${route}`, config);
        if (response.status === 401) {

      const refreshed = await refreshSession()

      if (refreshed) {

        return request(route, options)
      }
    }
    const data = await response.json().data
    return data
  }
  function addContact(contact_id) {
    contactList.push(getUserCredentials(contact_id))
  }
  return { getContacts, addContact, getUserCredentials }
})
export const useUserStore = defineStore('user', () => {

  // =====================================
  // STATE
  // =====================================

  const sessionKey = ref(
    localStorage.getItem('session_key')
  )

  const refreshKey = ref(
    localStorage.getItem('refresh_key')
  )

  const user = ref(null)

  // =====================================
  // GETTERS
  // =====================================

  const isAuthenticated = computed(() => {
    return !!sessionKey.value
  })

  // =====================================
  // ACTIONS
  // =====================================

  function saveTokens(access, refresh) {

    sessionKey.value = access
    refreshKey.value = refresh

    localStorage.setItem(
      'session_key',
      access
    )

    localStorage.setItem(
      'refresh_key',
      refresh
    )
  }

  function clearTokens() {

    sessionKey.value = null
    refreshKey.value = null
    user.value = null

    localStorage.removeItem('session_key')
    localStorage.removeItem('refresh_key')
    router.push('/');
  }

  async function login(username, password) {

    const response = await fetch(
      `${BASE_URL}/login`,
      {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          username,
          password
        })
      }
    )

    const data = await response.json()

    if (!response.ok) {
      throw new Error(data.message)
    }

    saveTokens(
      data.data.access_token,
      data.data.refresh_token
    )

    user.value = data.data.user

    return data
  }

  async function logout() {
    clearTokens()
  }
  async function fetchProfile() {
  const response = await fetch(
    `${BASE_URL}/profile`,
    {
      headers: {
        Authorization:
          `Bearer ${localStorage.getItem('session_key')}`
      }
    }
  )

  const data = await response.json()
  user.value = data.data
  console.log('User session key', localStorage.getItem('session_key'))
  console.log('Response', data.data)
  return data.data
}
  return {
    sessionKey,
    refreshKey,
    user,
    isAuthenticated,

    fetchProfile,
    saveTokens,
    clearTokens,
    login,
    logout
  }
})