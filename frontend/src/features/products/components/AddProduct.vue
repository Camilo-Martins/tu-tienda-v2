<script setup>
import { Form, Field, ErrorMessage } from 'vee-validate'
import BaseButton from '@/components/BaseButton.vue'
import { useAddProducto } from '../composables/composables'
import useToast from '@/stores/useToast'
import { productSchema } from '../schemas/productSchema'

const props = defineProps({
  proveedores: {
    type: Array,
    required: true,
  },
})

const { trigger } = useToast()
const { sendData: sendProducto } = useAddProducto()
const emit = defineEmits(['addProduct'])

const submit = async (values, { resetForm }) => {
  try {
    await sendProducto({
      nombre_producto: values.nombre_producto,
      descripcion: values.descripcion,
      precio: values.precio,
      stock_actual: values.stock,
      categoria: values.categoria ? values.categoria : 'NoDefinido',
      proveedor_id: values.proveedor,
    })

    emit('addProduct')
    resetForm()
  } catch (error) {
    trigger('Ingrese nombre para agregar el producto', 'error')
  }
}
</script>

<template>
  <div class="bg-white rounded-xl shadow-sm border border-slate-200 p-5 mb-8">
    <Form
      :validation-schema="productSchema"
      @submit="submit"
      class="grid grid-cols-1 md:grid-cols-12 gap-4 items-end"
    >
      <div class="form-field md:col-span-2">
        <label class="block pb-2">Nombre Producto</label>
        <Field
          type="text"
          name="nombre_producto"
          class="form-input"
          placeholder="Ej: Arroz Grano Largo"
        />
      </div>

      <div class="form-field md:col-span-2">
        <label class="block pb-2">Descripción</label>
        <Field
          type="text"
          name="descripcion"
          class="form-input"
          placeholder="Ej: Arroz de grano largo de calidad"
        />
      </div>

      <div class="form-field md:col-span-2">
        <label class="block pb-2">Precio</label>
        <Field
          type="number"
          name="precio"
          class="form-input"
          placeholder="Ej: 10000"
        />
      </div>

      <div class="form-field md:col-span-2">
        <label class="block pb-2">Categoría</label>
        <Field as="select" class="form-input" name="categoria">
          <option value="" disabled>Seleccione</option>
          <option value="">No definido</option>
          <option value="Alimentos">Alimentos</option>
          <option value="Bebidas">Bebidas</option>
          <option value="Limpieza">Limpieza</option>
          <option value="Higiene">Higiene Personal</option>
          <option value="Tecnologia">Tecnología</option>
          <option value="Escolares">Art. Escolares</option>
          <option value="Regalos">Regalos</option>
          <option value="Dulces">Dulces</option>
        </Field>
      </div>

      <div class="form-field md:col-span-2">
        <label class="block pb-2">Proveedor</label>
        <Field as="select" class="form-input" name="proveedor">
          <option value="" disabled>Seleccionar</option>
          <option
            v-for="proveedor in proveedores"
            :key="proveedor.id"
            :value="proveedor.id"
          >
            {{ proveedor.nombre_completo }} - ({{ proveedor.nombre_empresa }})
          </option>
        </Field>
      </div>

      <div class="form-field md:col-span-1">
        <label class="block pb-2">Stock</label>
        <Field
          type="number"
          name="stock"
          class="form-input"
          placeholder="Ej: 100"
        />
      </div>

      <div class="form-field md:col-span-1">
        <BaseButton class="w-full" label="Agregar Producto" type="submit">
          Agregar
        </BaseButton>
      </div>

      <div class="form-field col-span-12">
        <ErrorMessage name="nombre_producto" class=" text-red-600 italic" />
        <ErrorMessage name="precio" class=" text-red-600 italic" />
        <ErrorMessage name="stock" class=" text-red-600 italic" />
      </div>
    </Form>
  </div>
</template>

<style scoped></style>