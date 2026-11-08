<script setup>
import { computed } from 'vue'
import { useRouter, useRoute } from 'vue-router'

const router = useRouter()
const route = useRoute()

const storeName = computed(() => {
  return localStorage.getItem('user_tienda') || 'Mi tienda'
})

const logout = () => {
  localStorage.clear()
  router.push('/login')
}

const isActive = (name) => route.name === name
</script>

<template>
  <nav class="border-t border-blue-800 bg-blue-900/90 text-white shadow-sm">
    <div class="max-w-7xl mx-auto px-4 sm:px-8 py-4 flex flex-wrap items-center justify-between gap-3">
      <RouterLink to="/" class="nav-link px-5 hover:bg-white/20 transition px-3 py-1 rounded-md">
        <span class="text-base font-medium opacity-90 text-xl uppercase">
          {{ storeName }}
        </span>
      </RouterLink>

      <div class="flex w-full flex-wrap items-center justify-start gap-1 text-[11px] font-bold uppercase sm:w-auto sm:flex-1 sm:justify-end">
        <RouterLink to="/panel/personal" class="nav-link px-5 hover:bg-white/20 transition px-3 py-1 rounded-md"
          :class="{ 'nav-active': isActive('personal') }">
          Personal
        </RouterLink>

        <RouterLink to="/panel/proveedores" class="nav-link px-5 hover:bg-white/20 transition px-3 py-1 rounded-md"
          :class="{ 'nav-active': isActive('proveedor') }">
          Proveedores
        </RouterLink>

        <RouterLink to="/panel/productos" class="nav-link px-5 hover:bg-white/20 transition px-3 py-1 rounded-md"
          :class="{ 'nav-active': isActive('productos') }">
          Productos
        </RouterLink>
       
        <RouterLink to="/panel/ventas" class="nav-link px-5 hover:bg-white/20 transition px-3 py-1 rounded-md"
          :class="{ 'nav-active': isActive('ventas') }">
          Venta
        </RouterLink>
        <RouterLink to="/panel/historial-ventas" class="nav-link px-5 hover:bg-white/20 transition px-3 py-1 rounded-md"
          :class="{ 'nav-active': isActive('historial-ventas') }">
          Historial de venta
        </RouterLink>
        <RouterLink to="/panel/clientes" class="nav-link px-5 hover:bg-white/20 transition px-3 py-1 rounded-md"
          :class="{ 'nav-active': isActive('clientes') }">
          Clientes
        </RouterLink>
      </div>
    </div>
  </nav>
</template>
