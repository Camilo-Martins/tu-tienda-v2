// services/registerService.ts
export async function addHorarioService(body) {
  const response = await fetch(`${import.meta.env.VITE_API_URL}horarios/crear`, {
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

export async function getHorarioService(body) {
  const response = await fetch(`${import.meta.env.VITE_API_URL}horarios/obtener-horario`, {
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

export async function asignarPersonalService(id, body) {
  const response = await fetch(
    `${import.meta.env.VITE_API_URL}horarios/asignacion-personal/${id}`,
    {
      method: 'POST',
      headers: {
        'content-type': 'application/json',
      },
      body: JSON.stringify(body),
    },
  )

  const data = await response.json()

  if (!response.ok) {
    throw {
      status: response.status,
      data,
    }
  }

  return data
}

export async function desasignarPersonalService(id, body) {
  const response = await fetch(
    `${import.meta.env.VITE_API_URL}horarios/eliminacion-personal/${id}`,
    {
      method: 'POST',
      headers: {
        'content-type': 'application/json',
      },
      body: JSON.stringify(body),
    },
  )

  const data = await response.json()

  if (!response.ok) {
    throw {
      status: response.status,
      data,
    }
  }

  return data
}
