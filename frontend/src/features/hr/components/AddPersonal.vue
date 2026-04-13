<script setup>
import { Form, Field, ErrorMessage } from 'vee-validate'
import { useAddPersonal } from '../composables/useAddPersonal'
import BaseButton from '@/components/BaseButton.vue'

import useToast from '@/stores/useToast'
import { useAddHorario } from '../composables/useHorario'
import { personalSchema } from '../schemas/personalSchema'
const { trigger } = useToast()

const { sendData } = useAddPersonal()

const emit = defineEmits(['created', 'generated'])
const { sendData: sendHorario, error: errorHorario, data } = useAddHorario()

const submitHorario = async () => {
  try {
    await sendHorario()

    emit('generated')
  } catch (error) {
    trigger(errorHorario)
  }
}

const submit = async (values, { resetForm }) => {
  try {
    await sendData({
      nombre_completo: values.nombre_completo,
      telefono: values.telefono,
      rut: values.rut,
      pago_diario: values.pago_diario,
    })

    resetForm()
    emit('created')
  } catch (error) {
    trigger("Verifique que los datos tengan el formato correcto o no están asignados a otra persona")
  }
}
</script>

<template>
  <!-- Formulario -->
  <div class="grid grid-cols-12">
    <div class="col-span-12">
      <div class="bg-white rounded-xl shadow-sm border border-slate-200 p-5 mb-8">
       <Form
  :validation-schema="personalSchema"
  @submit="submit"
  class="grid grid-cols-1 md:grid-cols-12 gap-4 items-end"
>
  <div class="form-field md:col-span-3">
    <label class="block pb-2">Nombre</label>
    <Field
      type="text"
      name="nombre_completo"
      class="form-input"
      placeholder="Ej: Camilo Álvarez"
    />
  </div>

  <div class="form-field md:col-span-2">
    <label class="block pb-2">RUT</label>
    <Field type="text" name="rut" class="form-input" placeholder="Ej: 12.345.678-9" />
  </div>

  <div class="form-field md:col-span-2">
    <label class="block pb-2">Teléfono</label>
    <Field type="text" name="telefono" class="form-input" placeholder="33456784" />
  </div>

  <div class="form-field md:col-span-2">
    <label class="block pb-2">Monto Pago</label>
    <Field type="number" name="pago_diario" class="form-input" placeholder="Ej: 20000" />
  </div>

  <div class="form-field md:col-span-1">
    <BaseButton label="Agregar Personal" type="submit" class="w-full">
      Agregar
    </BaseButton>
  </div>

  <div class="form-field md:col-span-2">
    <BaseButton
      label="Generar Horario"
      class="w-full bg-green-800 hover:bg-green-900"
      type="button"
      @click="submitHorario"
    >
      Generar Horario
    </BaseButton>
  </div>

  <div class="form-field col-span-12">
    <ErrorMessage name="nombre_completo" class=" text-red-600 italic col-span-2 " />
    <ErrorMessage name="rut" class=" text-red-600 italic col-span-2 " />
    <ErrorMessage name="telefono" class=" text-red-600 italic col-span-2 " />
    <ErrorMessage name="pago_diario" class="text-red-600 italic col-span-2 " />
  </div>
</Form>
      </div>
    </div>
  </div>
</template>

<style scoped></style>
