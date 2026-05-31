<script setup>
defineProps({
  modelValue: String
})

const emit = defineEmits([
  'update:modelValue'
])
</script>

<template>

<input
  type="number"
  :value="modelValue"
  @input="emit('update:modelValue', $event.target.value)"
  placeholder="Search users by ID"
  class="search"
/>

</template>

<style scoped>
.search {
  width: 100%;
  padding: 1rem;
  border-radius: 12px;
  border: none;
  background: rgba(255,255,255,0.05);
  color: white;
}
</style>