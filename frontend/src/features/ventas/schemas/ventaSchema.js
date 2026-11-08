export function normalizePhone(value) {
  return String(value ?? '').replace(/\D/g, '')
}

export function validatePhone(value) {
  const raw = String(value ?? '').trim()
  const digits = normalizePhone(raw)
  return raw.length <= 30 && digits.length >= 8 && digits.length <= 15
}

export function validateQuantity(quantity, stock) {
  const parsedQuantity = Number(quantity)
  const parsedStock = Number(stock)
  return Number.isInteger(parsedQuantity) && parsedQuantity > 0 && parsedQuantity <= parsedStock
}

export function formatPrice(value) {
  return new Intl.NumberFormat('es-CL', {
    style: 'currency',
    currency: 'CLP',
    maximumFractionDigits: 0,
  }).format(Number(value) || 0)
}

export function formatDate(value) {
  if (!value) return '—'
  return new Intl.DateTimeFormat('es-CL', {
    dateStyle: 'short',
    timeStyle: 'short',
  }).format(new Date(value))
}
