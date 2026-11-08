<script setup>
import { onMounted, ref } from 'vue'
import useToast from '@/stores/useToast'
import { getCustomers, getSales } from '../services/ventasService'
import { formatDate, formatPrice } from '../schemas/ventaSchema'

const { trigger } = useToast()
const sales = ref([])
const customers = ref([])
const loading = ref(false)
const filters = ref({
  desde: '',
  hasta: '',
  cliente_id: '',
  tipo: '',
  orden: 'desc',
})

const loadCustomers = async () => {
  try {
    customers.value = await getCustomers()
  } catch (error) {
    trigger(error.message || 'No se pudieron cargar los clientes.')
  }
}

const loadSales = async () => {
  loading.value = true
  try {
    sales.value = await getSales(filters.value)
  } catch (error) {
    trigger(error.message || 'No se pudo cargar el historial.')
  } finally {
    loading.value = false
  }
}

const clearFilters = () => {
  filters.value = { desde: '', hasta: '', cliente_id: '', tipo: '', orden: 'desc' }
  loadSales()
}

onMounted(() => {
  loadSales()
  loadCustomers()
})
</script>

<template>
  <section class="mx-auto w-full max-w-7xl px-2 py-2 sm:px-4">
    <header class="mb-6">
      <p class="mb-1 text-sm font-semibold uppercase tracking-wide text-blue-700">Registro del negocio</p>
      <h1 class="text-2xl font-semibold text-slate-800 sm:text-3xl">Historial de venta</h1>
      <p class="mt-1 text-sm text-slate-500">Revisa ventas, artículos y pagos con filtros por fecha y cliente.</p>
    </header>

    <form class="mb-6 grid grid-cols-1 items-end gap-3 rounded-2xl border border-slate-200 bg-white p-4 shadow-sm sm:grid-cols-2 xl:grid-cols-6" @submit.prevent="loadSales">
      <label class="text-sm font-medium text-slate-700">Desde
        <input v-model="filters.desde" class="form-input mt-1" type="date" />
      </label>
      <label class="text-sm font-medium text-slate-700">Hasta
        <input v-model="filters.hasta" class="form-input mt-1" type="date" />
      </label>
      <label class="text-sm font-medium text-slate-700">Cliente
        <select v-model="filters.cliente_id" class="form-input mt-1">
          <option value="">Todos</option>
          <option v-for="customer in customers" :key="customer.id" :value="customer.id">{{ customer.nombre }} · {{ customer.telefono }}</option>
        </select>
      </label>
      <label class="text-sm font-medium text-slate-700">Tipo
        <select v-model="filters.tipo" class="form-input mt-1">
          <option value="">Todos</option>
          <option value="CONTADO">Pagadas</option>
          <option value="FIADO">Fiadas</option>
        </select>
      </label>
      <label class="text-sm font-medium text-slate-700">Orden por fecha
        <select v-model="filters.orden" class="form-input mt-1">
          <option value="desc">Más recientes</option>
          <option value="asc">Más antiguas</option>
        </select>
      </label>
      <div class="flex gap-2">
        <button class="flex-1 rounded-lg bg-blue-700 px-3 py-2.5 text-sm font-semibold text-white hover:bg-blue-800" type="submit">Filtrar</button>
        <button class="rounded-lg border border-slate-300 px-3 py-2.5 text-sm font-medium text-slate-700 hover:bg-slate-50" type="button" @click="clearFilters">Limpiar</button>
      </div>
    </form>

    <div class="overflow-hidden rounded-2xl border border-slate-200 bg-white shadow-sm">
      <div class="flex items-center justify-between border-b border-slate-200 px-5 py-4">
        <h2 class="font-semibold text-slate-800">Ventas registradas</h2>
        <span class="text-sm text-slate-500">{{ sales.length }} resultados</span>
      </div>
      <div v-if="loading" class="px-5 py-12 text-center text-slate-500">Cargando historial...</div>
      <div v-else-if="!sales.length" class="px-5 py-12 text-center text-slate-500">No hay ventas que coincidan con los filtros.</div>
      <div v-else class="overflow-x-auto">
        <table class="min-w-full divide-y divide-slate-200 text-sm">
          <thead class="bg-slate-50 text-left text-xs uppercase tracking-wide text-slate-500">
            <tr>
              <th class="px-5 py-3">Fecha</th>
              <th class="px-5 py-3">Tipo / cliente</th>
              <th class="px-5 py-3">Artículos</th>
              <th class="px-5 py-3 text-right">Total</th>
              <th class="px-5 py-3 text-right">Saldo pendiente</th>
            </tr>
          </thead>
          <tbody class="divide-y divide-slate-100">
            <tr v-for="sale in sales" :key="sale.id" class="align-top hover:bg-slate-50/70">
              <td class="whitespace-nowrap px-5 py-4 text-slate-600">{{ formatDate(sale.fecha) }}</td>
              <td class="px-5 py-4">
                <span class="rounded-full px-2.5 py-1 text-xs font-semibold" :class="sale.tipo === 'FIADO' ? 'bg-amber-100 text-amber-800' : 'bg-emerald-100 text-emerald-800'">{{ sale.tipo === 'FIADO' ? 'Fiada' : 'Pagada' }}</span>
                <p v-if="sale.cliente" class="mt-2 font-medium text-slate-800">{{ sale.cliente.nombre }}</p>
                <p v-if="sale.cliente" class="text-xs text-slate-500">{{ sale.cliente.telefono }}</p>
                <p v-else class="mt-2 text-xs text-slate-500">Sin cliente asociado</p>
              </td>
              <td class="min-w-64 px-5 py-4">
                <ul class="space-y-1 text-slate-600">
                  <li v-for="item in sale.items" :key="item.producto_id" class="flex justify-between gap-4">
                    <span>{{ item.cantidad }} × {{ item.nombre_producto }}</span>
                    <span class="whitespace-nowrap">{{ formatPrice(item.subtotal) }}</span>
                  </li>
                </ul>
              </td>
              <td class="whitespace-nowrap px-5 py-4 text-right font-semibold text-slate-800">{{ formatPrice(sale.total) }}</td>
              <td class="whitespace-nowrap px-5 py-4 text-right" :class="sale.saldo_pendiente ? 'font-semibold text-amber-800' : 'text-slate-500'">{{ formatPrice(sale.saldo_pendiente) }}</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </section>
</template>
