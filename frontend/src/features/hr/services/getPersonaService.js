// services/registerService.ts
export async function getPersonaService(id) {
  const response = await fetch(`${import.meta.env.VITE_API_URL}personal/persona/${id}`, {
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

  return data
}
