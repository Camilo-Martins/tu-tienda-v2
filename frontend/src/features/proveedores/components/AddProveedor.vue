<script setup>
import { Form, Field, ErrorMessage } from 'vee-validate'
import BaseButton from '@/components/BaseButton.vue'
import BaseInput from '@/components/BaseInput.vue'
import useToast from '@/stores/useToast'
import { useAddProveedor } from '../composables/composables'
import { proveedorSchema } from '../schemas/proveedorSchema'

const { trigger } = useToast()
const { sendData } = useAddProveedor()
const emit = defineEmits(['created'])

const submit = async (values, { resetForm }) => {
  try {
    await sendData({
      nombre_completo: values.nombre_completo,
      telefono: values.telefono,
      rut: values.rut,
      email: values.email,
      nombre_empresa: values.nombre_empresa,
    })

    resetForm()
    emit('created')
  } catch (error) {
    trigger('El teléfono o email ya existe, por favor ingrese uno diferente.', 'error')
  }
}
</script>

<template>
  <div class="bg-white rounded-xl shadow-sm border border-slate-200 p-5 mb-8">
    <Form
      :validation-schema="proveedorSchema"
      @submit="submit"
     class="grid grid-cols-1 md:grid-cols-12 gap-4 items-end"
    >
      <BaseInput
      label="Representante"
      name="nombre_completo"
      placeholder="Ej: Juan Carlos B"
      wrapperClass="md:col-span-12"
    />

      <BaseInput
      label="RUT"
      name="rut"
      placeholder="12.345.678-9"
      wrapperClass="md:col-span-12"
    />

      <BaseInput
      label="Teléfono"
      name="telefono"
      placeholder="9876543"
      wrapperClass="md:col-span-12"
    />

      <BaseInput
      label="Empresa"
      name="nombre_empresa"
      placeholder="Chanchito Feliz"
      wrapperClass="md:col-span-12"
    />
    
  <BaseInput
      label="Email"
      name="email"
      placeholder="correo@empresa.cl"
      wrapperClass="md:col-span-12"
    />

  

      <div class="form-field md:col-span-12">
        <BaseButton class="w-full" label="Agregar Proveedor" type="submit"> Agregar </BaseButton>
      </div>

      <div class="col-span-12 flex flex-col gap-1">
        <ErrorMessage name="nombre_completo" class="text-red-600 col-span-6 italic" />
        <ErrorMessage name="rut" class="text-red-600 col-span-6 italic" />
        <ErrorMessage name="telefono" class="text-red-600 col-span-6 italic" />
        <ErrorMessage name="nombre_empresa" class="text-red-600 col-span-6 italic" />
        <ErrorMessage name="email" class="text-red-600 col-span-6 italic" />
      </div>
    </Form>
  </div>
</template>

<style scoped></style>
