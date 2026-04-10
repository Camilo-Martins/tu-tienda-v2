import { createRouter, createWebHistory } from 'vue-router'

import PersonalView from '@/features/hr/views/PersonalView.vue'
import HorarioView from '@/features/hr/views/HorarioView.vue'
import Proveedor from '@/features/proveedores/Proveedor.vue'
import Productos from '@/features/products/Productos.vue'
import Error404 from '@/features/Error/views/Error404.vue'
import PrivateLayout from '@/components/layout/PrivateLayout.vue'
import Panel from '@/features/Panel.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      component: PrivateLayout,
      children: [
        {
          path: '/',
          name: 'panel',
          component: Panel,
        },
        {
          path: '/panel/personal',
          name: 'personal',
          component: PersonalView,
        },
        {
          path: '/panel/productos',
          name: 'productos',
          component: Productos,
        },
        {
          path: '/panel/proveedores',
          name: 'proveedores',
          component: Proveedor,
        },
        {
          path: '/panel/ventas',
          name: 'ventas',
          component: HorarioView,
        },
      ],
    },

    {
      path: '/:pathMatch(.*)*',
      name: 'pagina-no-encontrada',
      component: Error404,
    },
  ],
})

export default router
