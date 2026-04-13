<script setup>
import { Form, Field } from 'vee-validate'
import { ref } from 'vue'
import useToast from '@/stores/useToast'
import BaseButton from '@/components/BaseButton.vue'
import { useAddNota } from '@/features/notas/composables/composables'

const { trigger } = useToast()
const emit = defineEmits(['created'])
const { sendData: sendAddNota } = useAddNota()

const nombre_nota = ref('')
const observaciones = ref('')

const submit = async () => {
  try {
    await sendAddNota({
      nombre_nota: nombre_nota.value,
      observaciones: observaciones.value,
    })

    nombre_nota.value = ''
    observaciones.value = ''
    emit('created')
  } catch (error) {
    trigger('Nombre nota debe tener un nombre.')
  }
}
</script>

<template>
  
      <div class="bg-white rounded-xl shadow-sm border border-slate-200 p-5 mb-8">
        <Form @submit="submit" class="grid grid-cols-1 md:grid-cols-12 gap-4 items-end">
          <div class="form-field md:col-span-3">
            <label class="block pb-2">Nombre</label>
            <Field
              type="text"
              name="nombre_nota"
              class="form-input"
              v-model="nombre_nota"
              placeholder="Ej: Llamar a María"
            />
          </div>

          <div class="form-field md:col-span-7">
            <label class="block pb-2">Observaciones</label>
            <Field
              type="text"
              name="observaciones"
              class="form-input"
              v-model="observaciones"
              placeholder="María tiene las llaves de la bodega"
            />
          </div>

          <div class="form-field md:col-span-2">
            <BaseButton label="Agregar Nota" type="submit" class="w-full">
              Agregar
            </BaseButton>
          </div>
           <div class="form-field col-span-12">

           </div>
        </Form>
      </div>
  
</template>