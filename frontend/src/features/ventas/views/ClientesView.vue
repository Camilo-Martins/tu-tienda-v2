<script setup>
import { onMounted, ref } from 'vue'
import useToast from '@/stores/useToast'
import {
  addCustomerPayment,
  getCustomerPayments,
  getCustomerPurchases,
  getCustomer,
  getCustomers,
  updateCustomer,
} from '../services/ventasService'
import { formatDate, formatPrice } from '../schemas/ventaSchema'

const { trigger } = useToast()
const customers = ref([])
const selectedCustomer = ref(null)
const purchases = ref([])
const payments = ref([])
const searchText = ref('')
const stateFilter = ref('')
const loadingCustomers = ref(false)
const loadingDetails = ref(false)
const editing = ref(false)
const saving = ref(false)
const editForm = ref({ nombre: '', telefono: '' })
const paymentAmounts = ref({})

const loadCustomers = async () => {
  loadingCustomers.value = true
  try {
    customers.value = await getCustomers({ busqueda: searchText.value, estado: stateFilter.value })
    if (selectedCustomer.value) {
      const refreshed = customers.value.find((customer) => customer.id === selectedCustomer.value.id)
      if (refreshed) selectedCustomer.value = refreshed
    }
  } catch (error) {
    trigger(error.message || 'No se pudo cargar la lista de clientes.')
  } finally {
    loadingCustomers.value = false
  }
}

const selectCustomer = async (customer) => {
  selectedCustomer.value = customer
  editing.value = false
  editForm.value = { nombre: customer.nombre, telefono: customer.telefono }
  loadingDetails.value = true
  try {
    const [freshCustomer, customerPurchases, customerPayments] = await Promise.all([
      getCustomer(customer.id),
      getCustomerPurchases(customer.id),
      getCustomerPayments(customer.id),
    ])
    selectedCustomer.value = freshCustomer
    purchases.value = customerPurchases
    payments.value = customerPayments
    paymentAmounts.value = {}
  } catch (error) {
    trigger(error.message || 'No se pudo cargar el detalle del cliente.')
  } finally {
    loadingDetails.value = false
  }
}

const startEditing = () => {
  if (!selectedCustomer.value) return
  editForm.value = {
    nombre: selectedCustomer.value.nombre,
    telefono: selectedCustomer.value.telefono,
  }
  editing.value = true
}

const saveCustomer = async () => {
  if (!editForm.value.nombre.trim() || !editForm.value.telefono.trim()) {
    trigger('Nombre y teléfono son obligatorios.')
    return
  }
  saving.value = true
  try {
    const saved = await updateCustomer(selectedCustomer.value.id, {
      nombre: editForm.value.nombre.trim(),
      telefono: editForm.value.telefono,
    })
    selectedCustomer.value = saved
    editing.value = false
    await loadCustomers()
    await selectCustomer(saved)
    trigger('Datos del cliente actualizados.', 'success')
  } catch (error) {
    trigger(error.message || 'No se pudieron guardar los datos.')
  } finally {
    saving.value = false
  }
}

const registerPayment = async (sale) => {
  const amount = Number(paymentAmounts.value[sale.id])
  if (!Number.isInteger(amount) || amount <= 0) {
    trigger('El abono debe ser un monto entero mayor que cero.')
    return
  }
  if (amount > sale.saldo_pendiente) {
    trigger(`El abono no puede superar el saldo de ${formatPrice(sale.saldo_pendiente)}.`)
    return
  }
  try {
    await addCustomerPayment(selectedCustomer.value.id, { venta_id: sale.id, monto: amount })
    trigger('Abono registrado correctamente.', 'success')
    await selectCustomer(selectedCustomer.value)
    await loadCustomers()
  } catch (error) {
    trigger(error.message || 'No se pudo registrar el abono.')
    await selectCustomer(selectedCustomer.value)
    await loadCustomers()
  }
}

onMounted(loadCustomers)
</script>

<template>
  <section class="mx-auto w-full max-w-7xl px-2 py-2 sm:px-4">
    <header class="mb-6">
      <p class="mb-1 text-sm font-semibold uppercase tracking-wide text-blue-700">Cuentas de clientes</p>
      <h1 class="text-2xl font-semibold text-slate-800 sm:text-3xl">Clientes</h1>
      <p class="mt-1 text-sm text-slate-500">Consulta compras fiadas, edita los datos y registra abonos.</p>
    </header>

    <div class="grid grid-cols-1 items-start gap-6 xl:grid-cols-[minmax(280px,0.72fr)_minmax(0,1.5fr)]">
      <aside class="overflow-hidden rounded-2xl border border-slate-200 bg-white shadow-sm">
        <div class="space-y-3 border-b border-slate-200 p-4">
          <div class="flex items-center justify-between gap-2">
            <h2 class="font-semibold text-slate-800">Directorio</h2>
            <span class="text-xs text-slate-500">{{ customers.length }} clientes</span>
          </div>
          <input v-model="searchText" class="form-input" placeholder="Buscar por nombre..." @keyup.enter="loadCustomers" />
          <div class="flex gap-2">
            <select v-model="stateFilter" class="form-input">
              <option value="">Todos los estados</option>
              <option value="deuda">Con deuda</option>
              <option value="sin_deudas">Sin deudas</option>
            </select>
            <button class="rounded-lg border border-slate-300 px-3 text-sm font-medium text-slate-700 hover:bg-slate-50" type="button" @click="loadCustomers">Filtrar</button>
          </div>
        </div>
        <div v-if="loadingCustomers" class="p-6 text-center text-sm text-slate-500">Cargando clientes...</div>
        <div v-else-if="!customers.length" class="p-6 text-center text-sm text-slate-500">No hay clientes que coincidan. Los clientes se crean al registrar una venta fiada.</div>
        <ul v-else class="max-h-[70vh] divide-y divide-slate-100 overflow-y-auto">
          <li v-for="customer in customers" :key="customer.id">
            <button class="w-full px-4 py-3 text-left transition hover:bg-slate-50" :class="selectedCustomer?.id === customer.id ? 'bg-blue-50 ring-inset ring-2 ring-blue-100' : ''" type="button" @click="selectCustomer(customer)">
              <span class="flex items-start justify-between gap-3">
                <span class="min-w-0">
                  <span class="block truncate font-semibold text-slate-800">{{ customer.nombre }}</span>
                  <span class="mt-0.5 block text-xs text-slate-500">{{ customer.telefono }}</span>
                </span>
                <span class="shrink-0 rounded-full px-2 py-1 text-[11px] font-semibold" :class="customer.saldo_pendiente > 0 ? 'bg-amber-100 text-amber-800' : 'bg-emerald-100 text-emerald-800'">{{ customer.estado }}</span>
              </span>
              <span class="mt-2 block text-sm font-medium text-slate-700">Saldo: {{ formatPrice(customer.saldo_pendiente) }}</span>
            </button>
          </li>
        </ul>
      </aside>

      <div v-if="!selectedCustomer" class="rounded-2xl border border-dashed border-slate-300 bg-white px-6 py-16 text-center text-slate-500">
        Selecciona un cliente para ver sus compras y administrar sus datos.
      </div>

      <section v-else class="space-y-5">
        <article class="rounded-2xl border border-slate-200 bg-white p-5 shadow-sm sm:p-6">
          <div class="mb-4 flex flex-wrap items-start justify-between gap-3">
            <div>
              <p class="text-xs font-semibold uppercase tracking-wide text-slate-500">Ficha de cliente</p>
              <h2 class="mt-1 text-xl font-semibold text-slate-800">{{ selectedCustomer.nombre }}</h2>
            </div>
            <span class="rounded-full px-3 py-1.5 text-sm font-semibold" :class="selectedCustomer.saldo_pendiente > 0 ? 'bg-amber-100 text-amber-900' : 'bg-emerald-100 text-emerald-900'">{{ selectedCustomer.estado }}</span>
          </div>

          <form v-if="editing" class="grid grid-cols-1 gap-3 sm:grid-cols-2" @submit.prevent="saveCustomer">
            <label class="text-sm font-medium text-slate-700">Nombre
              <input v-model="editForm.nombre" class="form-input mt-1" maxlength="100" required />
            </label>
            <label class="text-sm font-medium text-slate-700">Teléfono
              <input v-model="editForm.telefono" class="form-input mt-1" inputmode="tel" maxlength="30" required />
            </label>
            <div class="flex justify-end gap-2 sm:col-span-2">
              <button class="rounded-lg border border-slate-300 px-4 py-2 text-sm font-medium text-slate-700 hover:bg-slate-50" type="button" @click="editing = false">Cancelar</button>
              <button class="rounded-lg bg-blue-700 px-4 py-2 text-sm font-semibold text-white hover:bg-blue-800 disabled:opacity-50" type="submit" :disabled="saving">{{ saving ? 'Guardando...' : 'Guardar cambios' }}</button>
            </div>
          </form>
          <div v-else class="flex flex-wrap items-center justify-between gap-3">
            <div>
              <p class="text-sm text-slate-600">{{ selectedCustomer.telefono }}</p>
              <p class="mt-3 text-sm text-slate-500">Saldo pendiente</p>
              <p class="text-2xl font-bold text-slate-900">{{ formatPrice(selectedCustomer.saldo_pendiente) }}</p>
            </div>
            <button class="rounded-lg border border-blue-200 px-4 py-2 text-sm font-semibold text-blue-800 hover:bg-blue-50" type="button" @click="startEditing">Editar datos</button>
          </div>
        </article>

        <div v-if="loadingDetails" class="rounded-2xl border border-slate-200 bg-white p-8 text-center text-slate-500">Cargando compras y abonos...</div>
        <template v-else>
          <article class="overflow-hidden rounded-2xl border border-slate-200 bg-white shadow-sm">
            <div class="flex items-center justify-between border-b border-slate-200 px-5 py-4">
              <h3 class="font-semibold text-slate-800">Compras fiadas</h3>
              <span class="text-sm text-slate-500">{{ purchases.length }} ventas</span>
            </div>
            <div v-if="!purchases.length" class="px-5 py-8 text-center text-sm text-slate-500">Este cliente aún no tiene compras fiadas.</div>
            <div v-else class="divide-y divide-slate-100">
              <article v-for="purchase in purchases" :key="purchase.id" class="p-5">
                <div class="flex flex-wrap items-start justify-between gap-3">
                  <div>
                    <p class="font-semibold text-slate-800">Venta #{{ purchase.id }} <span class="ml-1 text-xs font-normal text-slate-500">{{ formatDate(purchase.fecha) }}</span></p>
                    <ul class="mt-2 space-y-1 text-sm text-slate-600">
                      <li v-for="item in purchase.items" :key="item.producto_id">{{ item.cantidad }} × {{ item.nombre_producto }} · {{ formatPrice(item.subtotal) }}</li>
                    </ul>
                  </div>
                  <div class="text-right">
                    <p class="text-sm text-slate-500">Total {{ formatPrice(purchase.total) }}</p>
                    <p class="mt-1 font-semibold" :class="purchase.saldo_pendiente ? 'text-amber-800' : 'text-emerald-700'">Pendiente {{ formatPrice(purchase.saldo_pendiente) }}</p>
                  </div>
                </div>
                <form v-if="purchase.saldo_pendiente > 0" class="mt-4 flex flex-wrap items-end gap-2" @submit.prevent="registerPayment(purchase)">
                  <label class="w-full max-w-xs text-xs font-medium text-slate-600">Registrar abono
                    <input v-model="paymentAmounts[purchase.id]" class="form-input mt-1" type="number" min="1" :max="purchase.saldo_pendiente" step="1" :placeholder="`Hasta ${purchase.saldo_pendiente}`" />
                  </label>
                  <button class="rounded-lg bg-blue-700 px-4 py-2.5 text-sm font-semibold text-white hover:bg-blue-800" type="submit">Aplicar abono</button>
                </form>
                <p v-else class="mt-3 text-sm font-medium text-emerald-700">Venta saldada</p>
              </article>
            </div>
          </article>

          <article class="overflow-hidden rounded-2xl border border-slate-200 bg-white shadow-sm">
            <div class="border-b border-slate-200 px-5 py-4"><h3 class="font-semibold text-slate-800">Abonos registrados</h3></div>
            <div v-if="!payments.length" class="px-5 py-6 text-sm text-slate-500">Todavía no hay abonos.</div>
            <ul v-else class="divide-y divide-slate-100">
              <li v-for="payment in payments" :key="payment.id" class="flex justify-between gap-4 px-5 py-3 text-sm">
                <span class="text-slate-600">{{ formatDate(payment.fecha) }} · Venta #{{ payment.venta_id }}</span>
                <strong class="text-emerald-700">{{ formatPrice(payment.monto) }}</strong>
              </li>
            </ul>
          </article>
        </template>
      </section>
    </div>
  </section>
</template>
