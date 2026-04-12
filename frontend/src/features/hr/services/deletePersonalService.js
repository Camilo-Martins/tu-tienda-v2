// services/registerService.ts
export async function deletePersonalService(id) {
  const response = await fetch(`${import.meta.env.VITE_API_URL}personal/desactivar/${id}`, {
    method: 'PATCH',
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

  return data
}
