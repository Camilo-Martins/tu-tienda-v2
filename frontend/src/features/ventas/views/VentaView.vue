<script setup>
import { onMounted, ref } from 'vue'
import useToast from '@/stores/useToast'
import ProductPicker from '../components/ProductPicker.vue'
import { useVentaCart } from '../composables/useVentaCart'
import { createSale, getCustomers } from '../services/ventasService'
import { formatPrice, normalizePhone, validatePhone } from '../schemas/ventaSchema'

const { trigger } = useToast()
const {
  cart,
  search,
  filteredProducts,
  total,
  itemCount,
  cartHasStockIssues,
  loadingProducts,
  loadProducts,
  addProduct,
  adjustQuantity,
  removeItem,
  clearCart,
} = useVentaCart()

const saleType = ref('CONTADO')
const customerName = ref('')
const customerPhone = ref('')
const matchedCustomer = ref(null)
const searchingCustomer = ref(false)
const submitting = ref(false)

const resetCustomer = () => {
  matchedCustomer.value = null
  customerName.value = ''
}

const lookupCustomer = async () => {
  const phone = normalizePhone(customerPhone.value)
  if (!phone || !validatePhone(phone)) {
    resetCustomer()
    return
  }
  searchingCustomer.value = true
  try {
    const matches = await getCustomers({ telefono: phone })
    const found = Array.isArray(matches) ? matches[0] : null
    matchedCustomer.value = found || null
    customerName.value = found?.nombre || ''
  } catch (error) {
    trigger(error.message || 'No se pudo consultar el teléfono.')
  } finally {
    searchingCustomer.value = false
  }
}

const onPhoneInput = () => {
  if (matchedCustomer.value && normalizePhone(customerPhone.value) !== matchedCustomer.value.telefono) {
    resetCustomer()
  }
}

const changeSaleType = (type) => {
  saleType.value = type
  if (type === 'CONTADO') {
    customerPhone.value = ''
    resetCustomer()
  }
}

const submitSale = async () => {
  if (!cart.value.length) {
    trigger('Agrega al menos un producto a la venta.')
    return
  }
  if (saleType.value === 'FIADO') {
    if (!customerName.value.trim()) {
      trigger('Ingresa el nombre del cliente para registrar la venta fiada.')
      return
    }
    if (!validatePhone(customerPhone.value)) {
      trigger('Ingresa un teléfono válido de 8 a 15 dígitos.')
      return
    }
  }
  if (!window.confirm(`¿Confirmas la venta por ${formatPrice(total.value)}?`)) return

  submitting.value = true
  try {
    const payload = {
      tipo: saleType.value,
      items: cart.value.map((item) => ({
        producto_id: item.id,
        cantidad: item.quantity,
        precio_esperado: item.price,
      })),
    }
    if (saleType.value === 'FIADO') {
      payload.cliente = {
        nombre: customerName.value.trim(),
        telefono: normalizePhone(customerPhone.value),
      }
    }
    await createSale(payload)
    trigger('Venta registrada correctamente.', 'success')
    clearCart()
    changeSaleType('CONTADO')
    await loadProducts()
  } catch (error) {
    trigger(error.message || 'No se pudo registrar la venta.')
    await loadProducts()
  } finally {
    submitting.value = false
  }
}

onMounted(loadProducts)
</script>

<template>
  <section class="mx-auto w-full max-w-7xl px-2 py-2 sm:px-4">
    <header class="mb-6 flex flex-wrap items-end justify-between gap-3">
      <div>
        <p class="mb-1 text-sm font-semibold uppercase tracking-wide text-blue-700">Punto de venta</p>
        <h1 class="text-2xl font-semibold text-slate-800 sm:text-3xl">Nueva venta</h1>
        <p class="mt-1 text-sm text-slate-500">Busca productos, revisa el stock y confirma el cobro.</p>
      </div>
      <div class="rounded-xl border border-blue-100 bg-blue-50 px-4 py-2 text-sm text-blue-900">
        {{ itemCount }} {{ itemCount === 1 ? 'artículo' : 'artículos' }} en el carrito
      </div>
    </header>

    <div class="grid grid-cols-1 items-start gap-6 xl:grid-cols-[minmax(0,1.55fr)_minmax(360px,0.85fr)]">
      <ProductPicker
        v-model:search="search"
        :products="filteredProducts"
        :loading="loadingProducts"
        @add="addProduct"
      />

      <aside class="rounded-2xl border border-slate-200 bg-white p-4 shadow-sm sm:p-6">
        <div class="mb-4 flex items-center justify-between">
          <h2 class="text-lg font-semibold text-slate-800">Resumen</h2>
          <button v-if="cart.length" class="text-sm font-medium text-slate-500 hover:text-red-700" type="button" @click="clearCart">Vaciar</button>
        </div>

        <div v-if="!cart.length" class="mb-5 rounded-xl bg-slate-50 px-4 py-8 text-center text-sm text-slate-500">Selecciona productos para comenzar.</div>
        <div v-else class="mb-5 max-h-72 space-y-3 overflow-y-auto pr-1">
          <article v-for="item in cart" :key="item.id" class="rounded-xl border border-slate-100 p-3">
            <div class="flex items-start justify-between gap-3">
              <div class="min-w-0">
                <h3 class="truncate font-medium text-slate-800">{{ item.name }}</h3>
                <p class="mt-1 text-xs text-slate-500">{{ formatPrice(item.price) }} c/u · stock {{ item.stock }}</p>
                <p v-if="item.quantity > item.stock" class="mt-1 text-xs font-semibold text-red-700">Stock actualizado; reduce la cantidad o quita el artículo.</p>
              </div>
              <button class="shrink-0 text-xs font-medium text-slate-400 hover:text-red-700" type="button" @click="removeItem(item)">Quitar</button>
            </div>
            <div class="mt-3 flex items-center justify-between">
              <div class="inline-flex items-center rounded-lg border border-slate-200">
                <button class="px-3 py-1.5 text-slate-700 hover:bg-slate-50" type="button" :aria-label="`Quitar una unidad de ${item.name}`" @click="adjustQuantity(item, -1)">−</button>
                <span class="min-w-8 text-center text-sm font-semibold text-slate-800">{{ item.quantity }}</span>
                <button class="px-3 py-1.5 text-slate-700 hover:bg-slate-50" type="button" :aria-label="`Agregar una unidad de ${item.name}`" @click="adjustQuantity(item, 1)">+</button>
              </div>
              <strong class="text-sm text-slate-800">{{ formatPrice(item.price * item.quantity) }}</strong>
            </div>
          </article>
        </div>

        <div class="border-t border-slate-200 pt-4">
          <div class="mb-4 flex items-center justify-between text-lg font-bold text-slate-900"><span>Total</span><span>{{ formatPrice(total) }}</span></div>
          <fieldset class="mb-4">
            <legend class="mb-2 text-sm font-semibold text-slate-700">Forma de venta</legend>
            <div class="grid grid-cols-2 gap-2">
              <button class="rounded-lg border px-3 py-2.5 text-sm font-semibold transition" :class="saleType === 'CONTADO' ? 'border-blue-700 bg-blue-700 text-white' : 'border-slate-200 text-slate-700 hover:bg-slate-50'" type="button" @click="changeSaleType('CONTADO')">Pagar ahora</button>
              <button class="rounded-lg border px-3 py-2.5 text-sm font-semibold transition" :class="saleType === 'FIADO' ? 'border-blue-700 bg-blue-700 text-white' : 'border-slate-200 text-slate-700 hover:bg-slate-50'" type="button" @click="changeSaleType('FIADO')">Fiar</button>
            </div>
          </fieldset>

          <div v-if="saleType === 'FIADO'" class="mb-4 space-y-3 rounded-xl bg-blue-50/70 p-4">
            <p class="text-sm font-semibold text-blue-900">Datos del cliente</p>
            <label class="block text-sm font-medium text-slate-700">
              Teléfono
              <span class="mt-1 flex gap-2">
                <input v-model="customerPhone" class="form-input" inputmode="tel" maxlength="30" placeholder="+56 9 1234 5678" @input="onPhoneInput" @blur="lookupCustomer" />
                <button class="rounded-lg border border-blue-200 px-3 text-sm font-semibold text-blue-800 hover:bg-blue-100 disabled:opacity-50" type="button" :disabled="searchingCustomer || !customerPhone" @click="lookupCustomer">{{ searchingCustomer ? '...' : 'Buscar' }}</button>
              </span>
            </label>
            <label class="block text-sm font-medium text-slate-700">
              Nombre
              <input v-model="customerName" class="form-input mt-1" maxlength="100" :readonly="Boolean(matchedCustomer)" :class="matchedCustomer ? 'bg-slate-100' : ''" placeholder="Nombre completo" />
            </label>
            <p v-if="matchedCustomer" class="text-xs font-medium text-emerald-800">Cliente encontrado. Se usará el nombre registrado.</p>
            <p v-else-if="validatePhone(customerPhone)" class="text-xs text-slate-600">Si el teléfono no existe, se creará el cliente con estos datos.</p>
          </div>

          <button class="w-full rounded-lg bg-blue-700 px-4 py-3 text-sm font-semibold text-white transition hover:bg-blue-800 disabled:cursor-not-allowed disabled:opacity-50" type="button" :disabled="submitting || !cart.length || cartHasStockIssues" @click="submitSale">
            {{ submitting ? 'Registrando...' : saleType === 'FIADO' ? 'Registrar venta fiada' : 'Confirmar pago' }}
          </button>
        </div>
      </aside>
    </div>
  </section>
</template>
