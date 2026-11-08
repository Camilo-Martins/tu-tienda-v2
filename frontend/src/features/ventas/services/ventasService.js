const apiBaseUrl = import.meta.env.VITE_API_URL || 'http://localhost:8000/api/v1/'

function getErrorMessage(payload, status) {
  if (payload?.errors && typeof payload.errors === 'object') {
    const first = Object.entries(payload.errors)[0]
    if (first) {
      const detail = Array.isArray(first[1]) ? first[1][0] : first[1]
      return `${first[0]}: ${detail}`
    }
  }
  return payload?.msg || payload?.detail || `No se pudo completar la solicitud (${status}).`
}

async function request(path, options = {}) {
  if (!apiBaseUrl) throw new Error('Configura VITE_API_URL para conectar con la API.')
  const base = apiBaseUrl.replace(/\/+$/, '')
  const endpoint = path.replace(/^\/+/, '')

  const response = await fetch(`${base}/${endpoint}`, {
    ...options,
    headers: {
      'Content-Type': 'application/json',
      ...options.headers,
    },
  })
  const payload = await response.json().catch(() => ({}))

  if (!response.ok) throw new Error(getErrorMessage(payload, response.status))
  return payload?.data ?? payload
}

function queryString(values) {
  const params = new URLSearchParams()
  Object.entries(values).forEach(([key, value]) => {
    if (value !== '' && value !== null && value !== undefined) params.set(key, value)
  })
  const query = params.toString()
  return query ? `?${query}` : ''
}

export function getProducts() {
  return request('productos/obtener/')
}

export function createSale(payload) {
  return request('ventas/', { method: 'POST', body: JSON.stringify(payload) })
}

export function getSales(filters = {}) {
  return request(`ventas/${queryString(filters)}`)
}

export function getCustomers(filters = {}) {
  return request(`ventas/clientes/${queryString(filters)}`)
}

export function createCustomer(payload) {
  return request('ventas/clientes/', { method: 'POST', body: JSON.stringify(payload) })
}

export function getCustomer(id) {
  return request(`ventas/clientes/${id}/`)
}

export function updateCustomer(id, payload) {
  return request(`ventas/clientes/${id}/`, {
    method: 'PATCH',
    body: JSON.stringify(payload),
  })
}

export function getCustomerPurchases(id) {
  return request(`ventas/clientes/${id}/compras/`)
}

export function getCustomerPayments(id) {
  return request(`ventas/clientes/${id}/abonos/`)
}

export function addCustomerPayment(id, payload) {
  return request(`ventas/clientes/${id}/abonos/`, {
    method: 'POST',
    body: JSON.stringify(payload),
  })
}
