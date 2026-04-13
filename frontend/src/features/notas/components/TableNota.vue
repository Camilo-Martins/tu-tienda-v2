<script setup>
import { ref, onMounted } from 'vue'
import useToast from '@/stores/useToast'
import { useGetNota, useEditNota } from '@/features/notas/composables/composables'

const { trigger } = useToast()
const emit = defineEmits(['updateNota'])
const props = defineProps({
    notasList: {
        type: Array,
        required: true,
    },
})

const editing = ref({
    id: null,
    field: null,
    value: '',
})

const { sendData: sendEditNota } = useEditNota()

const startEdit = (nota, field) => {
    editing.value.id = nota.id
    editing.value.field = field
    editing.value.value = nota[field] ?? ''
}

const cancelEdit = () => {
    editing.value.id = null
    editing.value.field = null
    editing.value.value = ''
}

const saveEdit = async (nota) => {
    const { field, value } = editing.value

    if (!field) return

    if (value === nota[field]) {
        cancelEdit()
        return
    }

    const confirmed = window.confirm('¿Guardar cambios?')
    if (!confirmed) {
        cancelEdit()
        return
    }

    try {
        await sendEditNota(nota.id, {
            [field]: value,
        })

        nota[field] = value
         emit('updateNota')
    } catch (error) {
        trigger("Nombre nota no debe ser vacío.")
    } finally {
        cancelEdit()
    }
}

const toggleEstado = async (nota) => {
    const nuevoEstado = !nota.is_active

    const confirmed = window.confirm(
        `¿Deseas marcar esta nota como ${nuevoEstado ? 'Activa' : 'Inactiva'}?`,
    )
    if (!confirmed) return

    try {
        await sendEditNota(nota.id, {
            is_active: nuevoEstado,
        })

        nota.is_active = nuevoEstado
        emit('updateNota')
    } catch (error) { }
}
</script>

<template>
    <section>
        <div class="max-h-96 overflow-y-auto bg-white rounded-xl shadow-sm border border-slate-200">
            <table
                class="min-w-full border-collapse text-sm overflow-y-auto bg-white rounded-xl shadow-sm border border-slate-200">
                <thead class="bg-slate-100 text-slate-600">
                    <tr>
                        <th class="px-4 py-3 text-left" colspan="1">Nombre</th>
                        <th class="px-4 py-3 text-left" colspan="11">Detalle</th>
                        <th class="px-4 py-3 text-center" colspan="1">Estado</th>
                    </tr>
                </thead>

                <tbody>
                    <tr v-for="nota in notasList" :key="nota.id" class="border-t hover:bg-slate-200"
                        title="Haz doble clic para editar" :class="[
                            editing.id === nota.id ? 'bg-blue-100 ring-1 ring-blue-400' : 'hover:bg-slate-200',
                        ]">
                        <!-- NOMBRE -->
                        <td class="px-4 py-3 text-left truncate max-w-xs" colspan="1">
                            <input v-if="editing.id === nota.id && editing.field === 'nombre_nota'"
                                v-model="editing.value" type="text"
                                class="w-full rounded border border-slate-300 px-2 py-1" @blur="saveEdit(nota)"
                                @keyup.enter="saveEdit(nota)" @keyup.esc="cancelEdit" />

                            <span v-else class="block w-full cursor-pointer" @click="startEdit(nota, 'nombre_nota')">
                                {{ nota.nombre_nota }}
                            </span>
                        </td>

                        <!-- OBSERVACIONES -->
                        <td class="px-4 py-3 text-left truncate max-w-xs" colspan="11">
                            <textarea v-if="editing.id === nota.id && editing.field === 'observaciones'"
                                v-model="editing.value" rows="3"
                                class="w-full rounded border border-slate-300 px-2 py-1 resize-none"
                                @blur="saveEdit(nota)" @keyup.esc="cancelEdit"></textarea>

                            <span v-else class="block w-full cursor-pointer whitespace-pre-line"
                                @click="startEdit(nota, 'observaciones')">
                                {{ nota.observaciones ? nota.observaciones : 'Sin detalles' }}
                            </span>
                        </td>

                        <!-- ESTADO -->
                        <td class="px-4 py-3 text-center" colspan="1">
                            <button @click="toggleEstado(nota)" :class="nota.is_active
                                    ? 'px-3 py-1 text-sm rounded bg-green-100 text-green-700 hover:bg-green-200'
                                    : 'px-3 py-1 text-sm rounded bg-red-100 text-red-700 hover:bg-red-200'
                                ">
                                {{ nota.is_active ? 'Realizada' : 'Pendiente' }}
                            </button>
                        </td>
                    </tr>
                </tbody>
            </table>
        </div>
    </section>
</template>

<style scoped></style>
