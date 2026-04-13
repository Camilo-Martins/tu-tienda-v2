<script setup>
import { Form, Field, ErrorMessage } from 'vee-validate'
import BaseButton from '@/components/BaseButton.vue'
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
      <div class="form-field md:col-span-3">
        <label class="block pb-2">Representante</label>
        <Field
          type="text"
          name="nombre_completo"
          class="form-input"
          placeholder="Ej: Camilo Álvarez"
        />
      </div>

      <div class="form-field md:col-span-2">
        <label class="block pb-2">RUT</label>
        <Field
          type="text"
          name="rut"
          class="form-input"
          placeholder="Ej: 12345678-9"
        />
      </div>

      <div class="form-field md:col-span-2">
        <label class="block pb-2">Teléfono</label>
        <Field
          type="text"
          name="telefono"
          class="form-input"
          placeholder="56912345678"
        />
      </div>

      <div class="form-field md:col-span-2">
        <label class="block pb-2">Empresa</label>
        <Field
          type="text"
          name="nombre_empresa"
          class="form-input"
          placeholder="Ej: Distribuidora Sur"
        />
      </div>

      <div class="form-field md:col-span-2">
        <label class="block pb-2">Email</label>
        <Field
          type="text"
          name="email"
          class="form-input"
          placeholder="Ej: correo@empresa.cl"
        />
      </div>

      <div class="form-field md:col-span-1">
        <BaseButton class="w-full" label="Agregar Proveedor" type="submit">
          Agregar
        </BaseButton>
      </div>

      <div class="form-field col-span-12">
        <ErrorMessage name="nombre_completo" class="text-red-600 col-span-6 italic"/>
        <ErrorMessage name="rut" class="text-red-600 col-span-6 italic" />
        <ErrorMessage name="telefono" class="text-red-600 col-span-6 italic" />
        <ErrorMessage name="nombre_empresa" class="text-red-600 col-span-6 italic" />
        <ErrorMessage name="email" class="text-red-600 col-span-6 italic" />
      </div>
    </Form>
  </div>
</template>

<style scoped></style>