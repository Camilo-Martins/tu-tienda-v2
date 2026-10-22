# Frontend

Cliente Vue 3 + Vite. El código de producto se organiza por funcionalidad en `src/features/`; los componentes genéricos y el estado transversal viven en `src/components/` y `src/stores/`.

## Configuración

Crea `.env` con la URL base de la API, por ejemplo:

```env
VITE_API_URL=http://localhost:8000/api/v1/
```

## Comandos

```sh
npm install
npm run dev
npm run build
npm run lint
```

`npm run lint` informa problemas sin reescribir los archivos. Para formato automático usa `npm run format` de forma explícita.
