<script setup>
import { ref, onMounted } from 'vue'

import { useGetNota } from '@/features/notas/composables/composables'
import TableNota from './components/TableNota.vue'
import AddNota from './components/AddNota.vue'

const { sendData, data, loading, error } = useGetNota()
const editing = ref({
  id: null,
  field: null,
  value: '',
})

let notasList = ref([])

const getNota = async () => {
  await sendData()
  notasList.value = data.value.data
}

onMounted(() => {
  getNota()
})
</script>

<template>
  <section class="w-full px-6 py-6">
    <header class="mb-6">
      <h1 class="text-2xl font-semibold text-slate-800 uppercase">Agrega Recordatorios</h1>
    </header>

    <!-- Agregar una nota -->
    <div>
      <AddNota @created="getNota" />
    </div>

    <div>
      <TableNota :notasList="notasList" @updateNota="getNota" />
    </div>
  </section>
</template>

<style scoped></style>
