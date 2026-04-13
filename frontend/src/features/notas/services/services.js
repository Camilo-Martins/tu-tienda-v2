export async function getNota(body) {
  const response = await fetch(`${import.meta.env.VITE_API_URL}notas/obtener`, {
    method: 'GET',
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

// services/registerService.ts
export async function addNota(body) {
  const response = await fetch(`${import.meta.env.VITE_API_URL}notas/agregar`, {
    method: 'POST',
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

export async function editNota(id, body) {
  const response = await fetch(`${import.meta.env.VITE_API_URL}notas/editar/${id}`, {
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
