<script setup>
import { reactive } from 'vue'
import { formatPrice } from '../schemas/ventaSchema'

defineProps({
  products: { type: Array, default: () => [] },
  search: { type: String, default: '' },
  loading: { type: Boolean, default: false },
})

const emit = defineEmits(['update:search', 'add'])
const quantities = reactive({})

const quantityFor = (product) => quantities[product.id] ?? 1

const addSelectedQuantity = (product) => {
  const quantity = Number(quantityFor(product))
  if (!Number.isInteger(quantity) || quantity < 1 || quantity > Number(product.stock_actual)) return
  emit('add', product, quantity)
  quantities[product.id] = 1
}
</script>

<template>
  <section class="rounded-2xl border border-slate-200 bg-white p-4 shadow-sm sm:p-6">
    <div class="mb-4 flex flex-wrap items-center justify-between gap-3">
      <h2 class="text-lg font-semibold text-slate-800">Productos disponibles</h2>
      <label class="w-full sm:max-w-xs">
        <span class="sr-only">Buscar producto</span>
        <input :value="search" class="form-input" placeholder="Buscar por nombre..." type="search" @input="emit('update:search', $event.target.value)" />
      </label>
    </div>

    <div v-if="loading" class="rounded-xl bg-slate-50 px-4 py-10 text-center text-slate-500">Cargando productos...</div>
    <div v-else-if="!products.length" class="rounded-xl border border-dashed border-slate-300 px-4 py-10 text-center text-slate-500">
      {{ search ? 'No se encontraron productos para esa búsqueda.' : 'No hay productos con stock disponibles para la venta.' }}
    </div>
    <div v-else class="grid grid-cols-1 gap-3 sm:grid-cols-2 lg:grid-cols-3">
      <article
        v-for="product in products"
        :key="product.id"
        class="rounded-xl border border-slate-200 p-4 transition hover:border-blue-300 hover:bg-blue-50/40"
      >
        <span class="block truncate font-semibold text-slate-800">{{ product.nombre_producto }}</span>
        <span class="mt-1 block text-sm text-slate-500">{{ product.categoria || 'Sin categoría' }}</span>
        <span class="mt-4 flex items-center justify-between gap-2">
          <strong class="text-blue-800">{{ formatPrice(product.precio) }}</strong>
          <span class="rounded-full px-2.5 py-1 text-xs font-semibold" :class="Number(product.stock_actual) > 0 ? 'bg-emerald-50 text-emerald-700' : 'bg-red-50 text-red-700'">
            {{ Number(product.stock_actual) > 0 ? `Stock ${product.stock_actual}` : 'Sin stock' }}
          </span>
        </span>
        <div class="mt-4 flex items-center gap-2">
          <label class="sr-only" :for="`sale-quantity-${product.id}`">Cantidad de {{ product.nombre_producto }}</label>
          <input
            :id="`sale-quantity-${product.id}`"
            v-model.number="quantities[product.id]"
            class="form-input w-20"
            type="number"
            min="1"
            :max="product.stock_actual"
            placeholder="1"
            :aria-label="`Cantidad de ${product.nombre_producto}`"
          />
          <button
            class="flex-1 rounded-lg bg-blue-700 px-3 py-2 text-sm font-semibold text-white transition hover:bg-blue-800 disabled:cursor-not-allowed disabled:opacity-50"
            type="button"
            :disabled="Number(product.stock_actual) < 1 || quantityFor(product) < 1 || quantityFor(product) > product.stock_actual"
            @click="addSelectedQuantity(product)"
          >
            Agregar
          </button>
        </div>
      </article>
    </div>
  </section>
</template>
