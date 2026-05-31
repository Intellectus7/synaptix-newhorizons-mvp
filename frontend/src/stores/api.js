import { defineStore } from 'pinia'
import { useUserStore, useBaseUrl } from './user'

export const useApiStore = defineStore('api', () => {

  const userStore = useUserStore()
  const baseStore = useBaseUrl();
  const BASE_URL = baseStore.getBaseUrl();
  // =====================================
  // MAIN REQUEST FUNCTION
  // =====================================

  async function request(
    route = '/',
    options = {}
  ) {

    const method = options.method || 'GET'

    const headers = {
      'Content-Type': 'application/json',
      ...(options.headers || {})
    }

    // =====================================
    // AUTO JWT INJECTION
    // =====================================


      if (userStore.sessionKey) {
        headers['Authorization'] =
          `Bearer ${userStore.sessionKey}`
      }

      if (userStore.refreshKey) {
        headers['X-Refresh-Token'] =
          userStore.refreshKey
      }


    const response = await fetch(
      `${BASE_URL}${route}`,
      {
        ...options,
        method,
        headers,
        credentials: 'include'
      }
    )

    // =====================================
    // AUTO TOKEN REFRESH
    // =====================================

    if (response.status === 401) {

      const refreshed = await refreshSession()

      if (refreshed) {

        return request(route, options)
      }

      userStore.logout()

      throw new Error(
        'Session expired.'
      )
    }

    const data = await response.json()

    if (!response.ok) {
      throw new Error(
        data.message || 'Request failed.'
      )
    }

    return data
  }

  // =====================================
  // TOKEN REFRESH
  // =====================================

  async function refreshSession() {

    try {

      const response = await fetch(
        `${BASE_URL}/refresh`,
        {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'X-Refresh-Token':
              localStorage.getItem('refresh_key'),
              Authorization: `Bearer ${localStorage.getItem('refresh_key')}`
          }
        }
      )

      if (!response.ok) {
        return false
      }

      const data = await response.json()

      userStore.saveTokens(
        data.data.access_token,
        data.data.refresh_token
      )

      return true

    } catch {
      return false
    }
  }

  // =====================================
  // SHORTCUT METHODS
  // =====================================

  function get(route) {
    return request(route)
  }

  function post(route, body) {
    return request(route, {
      method: 'POST',
      body: JSON.stringify(body)
    })
  }

  function put(route, body) {
    return request(route, {
      method: 'PUT',
      body: JSON.stringify(body)
    })
  }

  function del(route) {
    return request(route, {
      method: 'DELETE'
    })
  }

  return {
    request,
    get,
    post,
    put,
    del
  }
})