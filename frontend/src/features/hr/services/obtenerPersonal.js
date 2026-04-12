// services/registerService.ts
export async function obtenerPersonal() {
  const response = await fetch(`${import.meta.env.VITE_API_URL}personal/obtener`, {
    method: 'GET',
    headers: {
      'content-type': 'application/json',
    },
    body: JSON.stringify(),
  })

  const data = await response.json()

  if (!response.ok) {
    throw {
      status: response.status,
      data,
    }
  }

  return data.data
}
