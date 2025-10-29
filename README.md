## Sistema de Gestión de Proyectos

Aplicación FastAPI + SQLModel para gestionar empleados, proyectos y asignaciones.


## Requisitos
- Python 3.10+
- FastAPI
- SQLModel
- Uvicorn

Instalar dependencias:
```bash
pip install -r requirements.txt
```
Ejecucion:
```bash
uvicorn app.main:app --reload

```
## Estructura de carpetas

-app/db.py → Conexión y creación de base de datos

-app/models.py → Modelos SQLModel

-app/schemas.py → Modelos Pydantic

-app/routers/ → Rutas de empleados, proyectos y asignaciones

-app/utils.py → Funciones auxiliares

## Reglas de negocio

-Un gerente no puede eliminarse si tiene proyectos activos.

-Los nombres de proyectos son únicos.

-Un empleado no puede asignarse dos veces al mismo proyecto.

-Soft delete (estado = False): los registros no se borran físicamente.

-Un empleado que ya sea gerente de un proyecto no puede ser asignado además como empleado del mismo proyecto.

## Códigos de Estado Usados

| Código | Significado | Cuándo se usa |
|:--------|:-------------|:-----------------------------|
| **200 OK** | Petición exitosa | Consultas (`GET`), actualizaciones (`PUT`), eliminaciones lógicas (`DELETE`) correctas |
| **201 Created** | Recurso creado correctamente | Creación de empleados, proyectos o asignaciones (`POST`) |
| **400 Bad Request** | Error de validación o regla de negocio | Cuando no se puede eliminar un gerente activo o datos inválidos |
| **404 Not Found** | Recurso no encontrado | Cuando no existe el empleado, proyecto o asignación solicitada |
| **409 Conflict** | Conflicto con los datos existentes | Nombre de proyecto duplicado o asignación repetida |


## Mapa de endpoints

### Empleados

| Método     | Ruta | Descripción | Parámetros / Body | Respuestas esperadas |
|:-----------|:------|:-------------|:------------------|:----------------------|
| **POST**   | `/empleados/` | Crear nuevo empleado | JSON `{ nombre, especialidad, salario, estado }` | `201 Created` con empleado creado |
| **GET**    | `/empleados/` | Listar empleados (con filtros) | Query: `especialidad`, `estado` | `200 OK` lista de empleados activos |
| **GET**    | `/empleados/{empleado_id}` | Obtener empleado por ID (incluye proyectos) | — | `200 OK` o `404 Not Found` |
| **PATCH**  | `/empleados/{empleado_id}` | Actualizar datos de empleado | JSON con campos a actualizar | `200 OK` o `404 Not Found` |
| **DELETE** | `/empleados/{empleado_id}` | Eliminar (soft delete) empleado | — | `200 OK` o `400` si es gerente activo |
| **GET**    | `/empleados/{empleado_id}/proyectos` | Consultar proyectos en los que participa el empleado | — | `200 OK` con lista de proyectos |

### Proyectos

| Método     | Ruta | Descripción | Parámetros / Body | Respuestas esperadas |
|:-----------|:------|:-------------|:------------------|:----------------------|
| **POST**   | `/proyectos/` | Crear proyecto con gerente | JSON `{ nombre, descripcion, presupuesto, gerente_id, estado }` | `201 Created` o `409 Conflict` si nombre duplicado |
| **GET**    | `/proyectos/` | Listar proyectos (con filtros) | Query: `estado`, `presupuesto_min`, `presupuesto_max` | `200 OK` lista de proyectos activos |
| **GET**    | `/proyectos/{proyecto_id}` | Obtener proyecto con gerente y empleados asignados | — | `200 OK` o `404 Not Found` |
| **PATCH**  | `/proyectos/{proyecto_id}` | Actualizar datos del proyecto | JSON con campos a actualizar | `200 OK` o `404 Not Found` |
| **DELETE** | `/proyectos/{proyecto_id}` | Eliminar (soft delete) proyecto | — | `200 OK` o `404 Not Found` |
| **GET**    | `/proyectos/{proyecto_id}/empleados` | Consultar empleados asignados a un proyecto | — | `200 OK` con lista de empleados |

### Asignaciones

| Método | Ruta | Descripción | Parámetros / Body | Respuestas esperadas |
|:--------|:------|:-------------|:------------------|:----------------------|
| **POST** | `/asignaciones/` | Asignar empleado a un proyecto | JSON `{ empleado_id, proyecto_id }` | `201 Created` o `409 Conflict` si ya asignado |
| **DELETE** | `/asignaciones/` | Desasignar empleado de un proyecto | JSON `{ empleado_id, proyecto_id }` | `200 OK` o `404 Not Found` |


