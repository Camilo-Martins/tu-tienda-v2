<script setup>
import { Form, Field } from 'vee-validate'
import { ref } from 'vue'
import useToast from '@/stores/useToast'
import BaseButton from '@/components/BaseButton.vue'
import { useAddNota } from '@/features/notas/composables/composables'
import BaseInput from '@/components/BaseInput.vue'

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

    <BaseInput
      label="Nombre"
      name="nombre_nota"
      v-model="nombre_nota"
      placeholder="Ej: Llamar a María"
      wrapperClass="md:col-span-12"
    />

    <BaseInput
      label="Observaciones"
      name="observaciones"
      v-model="observaciones"
      placeholder="María tiene las llaves del portón exterior"
      wrapperClass="md:col-span-12"
    />

    <div class="md:col-span-12">
      <BaseButton type="submit" class="w-full">
        Agregar
      </BaseButton>
    </div>

  </Form>
</div>
</template>