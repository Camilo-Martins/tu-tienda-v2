# Sistema de gestión de tienda

Aplicación para administrar productos, proveedores, personal, horarios, notas y publicidad. El proyecto mantiene el frontend y la API como aplicaciones separadas, con módulos organizados por dominio.

## Estructura

```text
.
├── backend/
│   ├── config/       # Configuración y puntos de entrada Django (ASGI/WSGI)
│   ├── productos/    # App Django de productos
│   ├── proveedores/
│   ├── personal/
│   ├── horarios/
│   ├── notas/
│   └── publicidad/
├── frontend/
│   └── src/
│       ├── features/ # Vistas, componentes y lógica por funcionalidad
│       ├── components/ # Componentes compartidos
│       ├── router/
│       └── stores/
├── .devcontainer/
└── docker-compose.yml
```

Cada app del backend es un límite de dominio independiente y contiene sus modelos, endpoints, servicios, migraciones y pruebas. El frontend agrupa su lógica de negocio bajo `features/`; lo reutilizable entre funcionalidades vive en `components/`, `stores/` y `assets/`.

## Iniciar con Docker

Requisitos: Docker y Docker Compose.

1. Copia `.env.example` como `.env` y ajusta las credenciales si lo necesitas.
2. Desde la raíz, ejecuta `docker compose up --build`.
3. Abre <http://localhost:5173/>. La API escucha en <http://localhost:8000/>.

Compose ejecuta las migraciones en un servicio de una sola ejecución antes de iniciar la API; así cada instancia del backend no intenta generar migraciones al arrancar.

La configuración Django está en `backend/config/`. Las variables de base de datos usan el prefijo `STORE_DB_` y la configuración de Compose asigna `store_db` como host dentro de la red de contenedores.

## Desarrollo local

Backend: crea un entorno virtual, instala `backend/requirements.txt` y ejecuta `python manage.py runserver` desde `backend/`.

Frontend: desde `frontend/`, ejecuta `npm install` y `npm run dev`. Define `VITE_API_URL` en `frontend/.env` para apuntar a la API.

## Tecnologías

- Backend: Django y Django REST Framework
- Frontend: Vue 3, Vite y Pinia
- Base de datos: MySQL
- Entorno local: Docker Compose

## Demo y autor

- [Video de demostración](https://youtu.be/2TB3V0x6M08)
- [LinkedIn](https://www.linkedin.com/in/camilo-martins-oliva/)
