// services/registerService.ts
export async function editPersonalServive(id, body) {
  const response = await fetch(`${import.meta.env.VITE_API_URL}personal/editar/${id}`, {
    method: 'PUT',
    headers: {
      'content-type': 'application/json',
    },
    body: JSON.stringify(body),
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
