<script setup>
import { onMounted } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()

onMounted(async () => {
  // redirigir después de confirmar
  setTimeout(() => {
    router.push('/')
  }, 500)
})
</script>

<template>
  <div class="w-full flex min-h-screen items-center justify-center px-4">
    <div class="w-full max-w-lg rounded-2xl bg-white p-8 shadow-xl space-y-6 border border-gray-200">
      <div>
        <h1 class="justify-center text-center font-bold uppercase text-2xl">
          Página no encontrada
        </h1>
        <h2 class="justify-center text-center">
          En unos segundos será redirigido al inicio de sesión
        </h2>
      </div>
    </div>
  </div>
</template>

<style scoped></style>
