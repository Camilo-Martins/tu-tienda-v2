<script setup>
import { ref } from 'vue'
import useToast from '@/stores/useToast'
import { useEditPersonal } from '../composables/useEditPersonal'

defineProps({
  items: {
    type: Array,
    required: true,
  },
  selectedId: {
    type: Number,
    default: null,
  },
})

const editing = ref({
  id: null,
  field: null,
  value: '',
})

const emit = defineEmits(['toggle-status', 'select', 'persona-data', 'updatedPersonal'])
const { trigger } = useToast()
const { sendData } = useEditPersonal()

const startEdit = (persona, field) => {
  editing.value.id = persona.id
  editing.value.field = field
  editing.value.value = persona[field] ?? ''
}

const cancelEdit = () => {
  editing.value.id = null
  editing.value.field = null
  editing.value.value = ''
}

const saveEdit = async (persona) => {
  const { field, value } = editing.value

  if (!field) return

  if (value === persona[field]) {
    cancelEdit()
    return
  }

  const confirmed = window.confirm('¿Guardar cambios?')
  if (!confirmed) {
    cancelEdit()
    return
  }

  try {
    await sendData(persona.id, {
      [field]: value,
    })

    emit('updatedPersonal')
    persona[field] = value
  } catch (error) {
    trigger("Verifique que el formato del campo ingresado sea correcto.")
  } finally {
    cancelEdit()
  }
}

const toggleEstado = async (persona) => {
  const nuevoEstado = !persona.is_active

  const confirmed = window.confirm(
    `¿Deseas marcar esta nota como ${nuevoEstado ? 'Activa' : 'Inactiva'}?`,
  )
  if (!confirmed) return

  try {
    await sendData(persona.id, {
      is_active: nuevoEstado,
    })

    persona.is_active = nuevoEstado
    emit('updatedPersonal')
  } catch (error) {
    trigger(error)
  }
}
</script>

<template>
  <div class="max-h-96 overflow-y-auto bg-white rounded-xl shadow-sm border border-slate-200">
    <div>
      <h5 class="text-center py-4 font-bold">Personal</h5>
    </div>
    <table
      class="min-w-full border-collapse text-sm overflow-y-auto bg-white rounded-xl shadow-sm border border-slate-200"
    >
      <thead class="bg-slate-100 text-slate-600">
        <tr>
          <th class="px-4 py-3 text-left">Nombre</th>
          <th class="px-4 py-3 text-center">Rut</th>
          
        
          <th class="px-4 py-3 text-center">Teléfono</th>
          <th class="px-4 py-3 text-center">Contactar</th>
          <th class="px-4 py-3 text-center">Pago</th>
            <th class="px-4 py-3 text-center">Estado</th>
        </tr>
      </thead>
      <tbody>
        <tr
          v-for="persona in items"
          :key="persona.id"
          class="border-t hover:bg-slate-50 transition cursor-pointer hover:bg-slate-200"
          title="Haz doble clic para editar"
          :class="[
            editing.id === persona.id ? 'bg-blue-100 ring-1 ring-blue-400' : 'hover:bg-slate-200',
          ]"
        >
          <td class="px-4 py-3 text-left">
            <input
              v-if="editing.id === persona.id && editing.field === 'nombre_completo'"
              v-model="editing.value"
              type="text"
              class="w-full rounded border border-slate-300 px-2 py-1"
              @blur="saveEdit(persona)"
              @keyup.enter="saveEdit(persona)"
              @keyup.esc="cancelEdit"
            />

            <span
              v-else
              class="block w-full cursor-pointer"
              @click="startEdit(persona, 'nombre_completo')"
            >
              {{ persona.nombre_completo ? persona.nombre_completo : 'No definido' }}
            </span>
          </td>
          <td class="px-4 py-3 text-center">
            <input
              v-if="editing.id === persona.id && editing.field === 'rut'"
              v-model="editing.value"
              type="text"
              class="w-full rounded border border-slate-300 px-2 py-1"
              @blur="saveEdit(persona)"
              @keyup.enter="saveEdit(persona)"
              @keyup.esc="cancelEdit"
            />

            <span v-else class="block w-full cursor-pointer" @click="startEdit(persona, 'rut')">
              {{ persona.rut ? persona.rut : 'No definido' }}
            </span>
          </td>

         
       

          <td class="px-4 py-3 text-center">
            <input
              v-if="editing.id === persona.id && editing.field === 'telefono'"
              v-model="editing.value"
              type="text"
              class="w-full rounded border border-slate-300 px-2 py-1"
              @blur="saveEdit(persona)"
              @keyup.enter="saveEdit(persona)"
              @keyup.esc="cancelEdit"
            />

            <span
              v-else
              class="block w-full cursor-pointer"
              @click="startEdit(persona, 'telefono')"
            >
              +{{ persona.telefono ? persona.telefono : 'No definido' }}
            </span>
          </td>
          <td class="px-4 py-3 text-center">
            <a
              :href="`https://wa.me/+569${persona.telefono.trim()}`"
              target="_blank"
              rel="noopener noreferrer"
              class="text-green-600 hover:underline font-medium"
            >
              WSP
            </a>
          </td>
           <td class="px-4 py-3 text-center">
            <input
              v-if="editing.id === persona.id && editing.field === 'pago_diario'"
              v-model="editing.value"
              type="text"
              class="w-full rounded border border-slate-300 px-2 py-1"
              @blur="saveEdit(persona)"
              @keyup.enter="saveEdit(persona)"
              @keyup.esc="cancelEdit"
            />

            <span
              v-else
              class="block w-full cursor-pointer"
              @click="startEdit(persona, 'pago_diario')"
            >
              ${{ persona.pago_diario ? persona.pago_diario : '0' }}
            </span>
          </td>
             <td class="px-4 py-3 text-center" colspan="1">
            <button
              @click="toggleEstado(persona)"
              :class="
                persona.is_active
                  ? 'px-3 py-1 text-sm rounded bg-green-100 text-green-700 hover:bg-green-200'
                  : 'px-3 py-1 text-sm rounded bg-red-100 text-red-700 hover:bg-red-200'
              "
            >
              {{ persona.is_active ? 'Activo' : 'Inactivo' }}
            </button>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<style scoped></style>
