import { computed, ref } from 'vue'
import useToast from '@/stores/useToast'
import { getProducts } from '../services/ventasService'

export function useVentaCart() {
  const { trigger } = useToast()
  const products = ref([])
  const cart = ref([])
  const search = ref('')
  const loadingProducts = ref(false)

  const filteredProducts = computed(() => {
    const query = search.value.trim().toLocaleLowerCase('es-CL')
    return products.value.filter((product) => {
      const hasPrice = product.precio !== null && product.precio !== undefined && Number.isFinite(Number(product.precio))
      const isActive = product.is_active !== false && product.is_active !== 0
      const availableForSale = isActive && hasPrice
      return availableForSale && (!query || product.nombre_producto?.toLocaleLowerCase('es-CL').includes(query))
    })
  })
  const total = computed(() => cart.value.reduce((sum, item) => sum + item.price * item.quantity, 0))
  const itemCount = computed(() => cart.value.reduce((sum, item) => sum + item.quantity, 0))
  const cartHasStockIssues = computed(() => cart.value.some((item) => item.quantity > item.stock))

  const loadProducts = async () => {
    loadingProducts.value = true
    try {
      const data = await getProducts()
      const productList = Array.isArray(data) ? data : data?.results ?? data?.data ?? []
      products.value = Array.isArray(productList) ? productList : []
      const currentProducts = new Map(products.value.map((product) => [product.id, product]))
      cart.value.forEach((item) => {
        const current = currentProducts.get(item.id)
        const isActive = current && current.is_active !== false && current.is_active !== 0
        item.stock = isActive ? Number(current.stock_actual || 0) : 0
        if (current && current.precio !== null) item.price = Number(current.precio)
      })
    } catch (error) {
      trigger(error.message || 'No se pudieron cargar los productos.')
    } finally {
      loadingProducts.value = false
    }
  }

  const addProduct = (product, requestedQuantity = 1) => {
    const stock = Number(product.stock_actual || 0)
    const quantity = Number(requestedQuantity)
    const existing = cart.value.find((item) => item.id === product.id)
    if (!Number.isInteger(quantity) || quantity < 1) {
      trigger('Ingresa una cantidad válida para agregar el producto.')
      return
    }
    if (stock <= 0) {
      trigger(`${product.nombre_producto} no tiene stock disponible.`)
      return
    }
    if (existing) {
      if (existing.quantity + quantity > stock) {
        trigger(`Stock insuficiente. Disponible: ${stock}.`)
        return
      }
      existing.quantity += quantity
      return
    }
    cart.value.push({
      id: product.id,
      name: product.nombre_producto,
      price: Number(product.precio || 0),
      stock,
      quantity,
    })
  }

  const adjustQuantity = (item, delta) => {
    const next = item.quantity + delta
    if (next < 1) {
      cart.value = cart.value.filter((entry) => entry.id !== item.id)
      return
    }
    if (next > item.stock) {
      trigger(`Stock insuficiente para ${item.name}. Disponible: ${item.stock}.`)
      return
    }
    item.quantity = next
  }

  const removeItem = (item) => {
    cart.value = cart.value.filter((entry) => entry.id !== item.id)
  }

  const clearCart = () => {
    cart.value = []
  }

  return {
    products,
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
  }
}
