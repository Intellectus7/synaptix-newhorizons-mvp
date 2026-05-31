<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useBaseUrl } from '@/stores/user'

const username = ref('')
const password = ref('')
const baseUrl = useBaseUrl();

const router = useRouter()

async function submitForm() {

    try {

        const response = await fetch(
            `${baseUrl.getBaseUrl()}/login`,
            {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                credentials: 'include',
                body: JSON.stringify({
                    username: username.value,
                    password: password.value
                })
            }
        )

        const data = await response.json()

        console.log(data)

        if (response.ok) {

            localStorage.setItem(
                'access_token',
                data.data.access_token
            )

            localStorage.setItem(
                'refresh_token',
                data.data.refresh_token
            )

            router.push('/')
        }

    } catch (err) {
        console.error(err)
    }
}
</script>

<template>
<div class="flex flex-col items-center absolute w-screen h-screen top-40">
    <div class="justify-center items-center bg-black  relative center">
        <span class="big-space"></span>
        <form @submit.prevent="submitForm" class="relative items-center  max-h-screen p-6 center">
            <h1 class="text-2xl text-blue-400 center"> Log in to Synaptix </h1>
            <label for="username"> Enter your username: </label>
            <span class="space"></span>
            <input type="text" id="username" class="input" v-model="username"/>
            <span class="space"></span>
            <br>
            <label for="password"> Enter your password: </label>
            <span class="space"></span>
            <input type="text" id="password" class="input" v-model="password"/>
            <button type="submit" class="btn">Submit</button>
        </form>
    </div>
</div>
</template>

<style scoped>
form {
    border-radius: 5px;
}
.center {
    position: center;
    padding: 10px;
    border-radius: 2px;
}
.space {
    padding: 5px;
}
.big-space {
    padding: 10px;
}
</style>