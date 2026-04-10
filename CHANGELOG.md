# Changelog

## [2.0] - Sin registro

### Servicios

- Antes: Registro, RRHH y Productos funcionaban en contenedores independientes
- Ahora: Todos conviven dentro del mismo contenedor

### Registro e inicio de sesión

- Antes: El sistema requiere registro, confirmación de cuenta e inicio de sesión
- Ahora: El sistema ya no requiere inicio de sesión. El usuario puede acceder directamente a la plataforma sin prerequisitos

### Validaciones generales

- Antes: El sistema era mas flexible, perimientiendo al usuario ingresar telefono y rut en personal o proveedor de forma flexible
- Ahora: El sistema ahora es mas rigido y tiene dos escenario permitido posibles:
  1. El usuario no ingresa Rut o Telefono (Permitido)
  2. El usuario ingresa Rut o Telefono formato correcto (Permitido)
  3. El usuario ingresa Rut o Telefono de forma incorrecta (No permitido)

- Antes: El sistema valida que el Rut o Telefono no se repita en la cuenta de un usuario, pero si en el sistems
- Ahora: Validación modificada: Ahora verifica que el Rut o telefono no se encuentre en el sistema

- Antes: Bienvenida y nombre personalizado para la vista privada de la imagen
- Ahora: Nombre por defecto del Sistema

### Seguridad

- Antes: Las rutas privadas estaban protegidas por JWT
- Ahora: Ya no existen rutas protegidas
