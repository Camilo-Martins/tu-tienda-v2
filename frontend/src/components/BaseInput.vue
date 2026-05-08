<script setup>
defineProps({
  label: String,
  name: String,
  type: {
    type: String,
    default: 'text'
  },
  placeholder: String,
  modelValue: String,
  wrapperClass: {
    type: String,
    default: ''
  }
})

const emit = defineEmits(['update:modelValue'])
import { Field } from 'vee-validate'
</script>

<template>
  <div :class="wrapperClass">
    <label class="block pb-2">{{ label }}</label>

    <Field
      :type="type"
      :name="name"
      class="form-input"
      :placeholder="placeholder"
      :modelValue="modelValue"
      @update:modelValue="emit('update:modelValue', $event)"
    />
  </div>
</template>
