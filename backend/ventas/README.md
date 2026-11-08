# Ventas API: rutas y solicitudes de ejemplo

La base URL es `/api/v1/ventas/`. Las ventas guardan sus artículos y el precio unitario aplicado; el valor se lee del producto desde el servidor. Una venta fiada requiere cliente. El teléfono se almacena solo con dígitos, por lo que volver a enviar un teléfono existente reutiliza el cliente y su nombre registrado.

## Endpoints

| Método | Ruta | Uso |
|---|---|---|
| `GET` | `/api/v1/ventas/` | Historial. Filtros: `desde`, `hasta`, `cliente_id`, `tipo=CONTADO\|FIADO`, `orden=asc\|desc`. |
| `POST` | `/api/v1/ventas/` | Registrar venta pagada o fiada; valida stock y lo descuenta atómicamente. |
| `GET` | `/api/v1/ventas/{id}/` | Ver venta con sus artículos y abonos. |
| `GET` | `/api/v1/ventas/clientes/` | Lista/búsqueda por `busqueda`, `telefono`; filtra `estado=deuda\|sin_deudas`. |
| `POST` | `/api/v1/ventas/clientes/` | Crear cliente. |
| `GET` | `/api/v1/ventas/clientes/{id}/` | Ver cliente y saldo calculado. |
| `PATCH` | `/api/v1/ventas/clientes/{id}/` | Editar nombre o teléfono. |
| `GET` | `/api/v1/ventas/clientes/{id}/compras/` | Compras asociadas al cliente. |
| `GET` | `/api/v1/ventas/clientes/{id}/abonos/` | Historial de abonos. |
| `POST` | `/api/v1/ventas/clientes/{id}/abonos/` | Abonar a una venta fiada del cliente. |

## Datos de ejemplo para envío manual

Usa un `producto_id` real devuelto por `GET /api/v1/productos/obtener/` y copia su precio a `precio_esperado`. Si el precio cambia desde que se cargó el carrito, el backend rechaza la venta para que se revise antes de cobrar. Estos son ejemplos de solicitudes, no se insertan automáticamente.

Para preparar un producto de muestra, crea primero un proveedor y copia el `id` devuelto:

`POST /api/v1/proveedores/agregar`

```json
{
  "nombre_completo": "Proveedor Demo",
  "nombre_empresa": "Distribuidora Demo",
  "telefono": "91234567"
}
```

Después crea un producto con el ID real del proveedor:

`POST /api/v1/productos/agregar`

```json
{
  "nombre_producto": "Agua 500 ml",
  "proveedor_id": 1,
  "precio": 1200,
  "stock_actual": 8,
  "categoria": "Bebidas"
}
```

Sustituye `proveedor_id: 1` por el ID que devolvió la primera solicitud. Luego comprueba stock cero o insuficiente intentando vender una cantidad mayor a la disponible; el backend devolverá `409` y no registrará esa venta.

Venta pagada:

```json
{
  "tipo": "CONTADO",
  "items": [
    { "producto_id": 1, "cantidad": 2, "precio_esperado": 1200 },
    { "producto_id": 3, "cantidad": 1, "precio_esperado": 800 }
  ]
}
```

Venta fiada (el teléfono puede enviarse con o sin espacios/signos):

```json
{
  "tipo": "FIADO",
  "cliente": { "nombre": "María Pérez", "telefono": "+56 9 1234 5678" },
  "items": [{ "producto_id": 1, "cantidad": 2, "precio_esperado": 1200 }]
}
```

Para abonar `500` pesos a la venta fiada `25` del cliente `7`:

```json
{ "venta_id": 25, "monto": 500 }
```

Ejemplo de edición de cliente:

```json
{ "nombre": "María Pérez Soto", "telefono": "56912345678" }
```
