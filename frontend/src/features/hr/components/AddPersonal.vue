<script setup>
import { Form, Field, ErrorMessage } from 'vee-validate'
import { useAddPersonal } from '../composables/useAddPersonal'
import BaseButton from '@/components/BaseButton.vue'
import BaseInput from '@/components/BaseInput.vue'

import useToast from '@/stores/useToast'
import { useAddHorario } from '../composables/useHorario'
import { personalSchema } from '../schemas/personalSchema'

const { trigger } = useToast()
const { sendData } = useAddPersonal()

const emit = defineEmits(['created', 'generated'])
const { sendData: sendHorario, error: errorHorario } = useAddHorario()

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
  <div class="grid grid-cols-12">
    <div class="col-span-12">
      <div class="bg-white rounded-xl shadow-sm border border-slate-200 p-5 mb-8">

        <Form
          :validation-schema="personalSchema"
          @submit="submit"
          class="grid grid-cols-1 md:grid-cols-12 gap-4 items-end"
        >

          <!-- Nombre -->
          <BaseInput
            label="Nombre"
            name="nombre_completo"
            placeholder="Beatriz"
            wrapperClass="md:col-span-12"
          />

          <!-- RUT -->
          <BaseInput
            label="RUT"
            name="rut"
            placeholder="12.345.678-9"
            wrapperClass="md:col-span-12"
          />

          <!-- Teléfono -->
          <BaseInput
            label="Teléfono"
            name="telefono"
            placeholder="33456784"
            wrapperClass="md:col-span-12"
          />

          <!-- Pago diario -->
          <BaseInput
            label="Monto Pago"
            name="pago_diario"
            placeholder="20000"
            wrapperClass="md:col-span-12"
          />

          <!-- Botón agregar -->
          <div class="md:col-span-12">
            <BaseButton type="submit" class="w-full">
              Agregar
            </BaseButton>
          </div>

          <!-- Botón generar -->
          <div class="md:col-span-12">
            <BaseButton
              type="button"
              class="w-full bg-green-800 hover:bg-green-900"
              @click="submitHorario"
            >
              Generar Horario
            </BaseButton>
          </div>

          <!-- Errores -->
          <div class="col-span-12 flex flex-col gap-1">
            <ErrorMessage name="nombre_completo" class="text-red-600 italic" />
            <ErrorMessage name="rut" class="text-red-600 italic" />
            <ErrorMessage name="telefono" class="text-red-600 italic" />
            <ErrorMessage name="pago_diario" class="text-red-600 italic" />
          </div>

        </Form>

      </div>
    </div>
  </div>
</template>