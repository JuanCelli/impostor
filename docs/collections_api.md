# Character Collections API

Endpoints HTTP para CRUD completo de Colecciones de Personajes con gestión de Characters asociados.

## Base URL

```
/api/v1/collections
```

## Modelos

### Character

```json
{
  "id": 1,
  "name": "string",
  "image_url": "string (opcional)",
  "collection_id": 1,
  "created_at": "2024-02-11T10:30:00",
  "updated_at": "2024-02-11T10:30:00"
}
```

### CharacterCollection

```json
{
  "id": 1,
  "name": "string",
  "image_url": "string (opcional)",
  "characters": [
    {
      "id": 1,
      "name": "string",
      "image_url": "string (opcional)",
      "collection_id": 1,
      "created_at": "2024-02-11T10:30:00",
      "updated_at": "2024-02-11T10:30:00"
    }
  ],
  "created_at": "2024-02-11T10:30:00",
  "updated_at": "2024-02-11T10:30:00"
}
```

## Endpoints de Colecciones

### 1. Crear una colección

**POST** `/api/v1/collections/`

Crea una nueva colección de personajes con opción de agregar personajes iniciales.

#### Request

```json
{
  "name": "Mi Colección",
  "image_url": "https://example.com/image.jpg",
  "characters": [
    {
      "name": "Personaje 1",
      "image_url": "https://example.com/char1.jpg"
    },
    {
      "name": "Personaje 2",
      "image_url": "https://example.com/char2.jpg"
    }
  ]
}
```

#### Response (201 Created)

```json
{
  "id": 1,
  "name": "Mi Colección",
  "image_url": "https://example.com/image.jpg",
  "created_at": "2024-02-11T10:30:00",
  "updated_at": "2024-02-11T10:30:00"
}
```

---

### 2. Obtener todas las colecciones

**GET** `/api/v1/collections/`

Obtiene un listado paginado de todas las colecciones (sin incluir sus personajes).

#### Query Parameters

- `skip` (int, optional, default: 0): Número de elementos a saltar
- `limit` (int, optional, default: 100): Número máximo de elementos (máximo: 1000)

#### Response (200 OK)

```json
{
  "total": 5,
  "skip": 0,
  "limit": 100,
  "items": [
    {
      "id": 1,
      "name": "Mi Colección",
      "image_url": "https://example.com/image.jpg",
      "created_at": "2024-02-11T10:30:00",
      "updated_at": "2024-02-11T10:30:00"
    }
  ]
}
```

---

### 3. Obtener una colección con sus personajes

**GET** `/api/v1/collections/{collection_id}`

Obtiene los detalles de una colección específica incluyendo todos sus personajes.

#### Path Parameters

- `collection_id` (int): ID de la colección

#### Response (200 OK)

```json
{
  "id": 1,
  "name": "Mi Colección",
  "image_url": "https://example.com/image.jpg",
  "characters": [
    {
      "id": 1,
      "name": "Personaje 1",
      "image_url": "https://example.com/char1.jpg",
      "collection_id": 1,
      "created_at": "2024-02-11T10:30:00",
      "updated_at": "2024-02-11T10:30:00"
    }
  ],
  "created_at": "2024-02-11T10:30:00",
  "updated_at": "2024-02-11T10:30:00"
}
```

#### Response (404 Not Found)

```json
{
  "detail": "Colección no encontrada"
}
```

---

### 4. Actualizar una colección

**PUT** `/api/v1/collections/{collection_id}`

Actualiza una colección existente. Solo se actualizan los campos proporcionados.

#### Path Parameters

- `collection_id` (int): ID de la colección

#### Request

```json
{
  "name": "Nombre Actualizado",
  "image_url": "https://example.com/new-image.jpg"
}
```

#### Response (200 OK)

```json
{
  "id": 1,
  "name": "Nombre Actualizado",
  "image_url": "https://example.com/new-image.jpg",
  "created_at": "2024-02-11T10:30:00",
  "updated_at": "2024-02-11T10:35:00"
}
```

---

### 5. Eliminar una colección

**DELETE** `/api/v1/collections/{collection_id}`

Elimina una colección existente y todos sus personajes asociados (cascada).

#### Path Parameters

- `collection_id` (int): ID de la colección

#### Response (204 No Content)

Sin contenido en el body.

#### Response (404 Not Found)

```json
{
  "detail": "Colección no encontrada"
}
```

---

## Endpoints de Personajes

### 6. Agregar un personaje a una colección

**POST** `/api/v1/collections/{collection_id}/characters`

Crea y agrega un nuevo personaje a una colección existente.

#### Path Parameters

- `collection_id` (int): ID de la colección

#### Request

```json
{
  "name": "Nuevo Personaje",
  "image_url": "https://example.com/new-char.jpg"
}
```

#### Response (201 Created)

```json
{
  "id": 2,
  "name": "Nuevo Personaje",
  "image_url": "https://example.com/new-char.jpg",
  "collection_id": 1,
  "created_at": "2024-02-11T10:35:00",
  "updated_at": "2024-02-11T10:35:00"
}
```

---

### 7. Obtener personajes de una colección

**GET** `/api/v1/collections/{collection_id}/characters`

Obtiene un listado paginado de todos los personajes de una colección.

#### Path Parameters

- `collection_id` (int): ID de la colección

#### Query Parameters

- `skip` (int, optional, default: 0): Número de elementos a saltar
- `limit` (int, optional, default: 100): Número máximo de elementos (máximo: 1000)

#### Response (200 OK)

```json
{
  "total": 2,
  "skip": 0,
  "limit": 100,
  "items": [
    {
      "id": 1,
      "name": "Personaje 1",
      "image_url": "https://example.com/char1.jpg",
      "collection_id": 1,
      "created_at": "2024-02-11T10:30:00",
      "updated_at": "2024-02-11T10:30:00"
    },
    {
      "id": 2,
      "name": "Personaje 2",
      "image_url": "https://example.com/char2.jpg",
      "collection_id": 1,
      "created_at": "2024-02-11T10:35:00",
      "updated_at": "2024-02-11T10:35:00"
    }
  ]
}
```

---

### 8. Obtener un personaje específico

**GET** `/api/v1/collections/{collection_id}/characters/{character_id}`

Obtiene los detalles de un personaje específico.

#### Path Parameters

- `collection_id` (int): ID de la colección (para validación)
- `character_id` (int): ID del personaje

#### Response (200 OK)

```json
{
  "id": 1,
  "name": "Personaje 1",
  "image_url": "https://example.com/char1.jpg",
  "collection_id": 1,
  "created_at": "2024-02-11T10:30:00",
  "updated_at": "2024-02-11T10:30:00"
}
```

---

### 9. Actualizar un personaje

**PUT** `/api/v1/collections/{collection_id}/characters/{character_id}`

Actualiza un personaje existente.

#### Path Parameters

- `collection_id` (int): ID de la colección (para validación)
- `character_id` (int): ID del personaje

#### Request

```json
{
  "name": "Personaje Actualizado",
  "image_url": "https://example.com/updated-char.jpg"
}
```

#### Response (200 OK)

```json
{
  "id": 1,
  "name": "Personaje Actualizado",
  "image_url": "https://example.com/updated-char.jpg",
  "collection_id": 1,
  "created_at": "2024-02-11T10:30:00",
  "updated_at": "2024-02-11T10:40:00"
}
```

---

### 10. Eliminar un personaje

**DELETE** `/api/v1/collections/{collection_id}/characters/{character_id}`

Elimina un personaje de una colección.

#### Path Parameters

- `collection_id` (int): ID de la colección (para validación)
- `character_id` (int): ID del personaje a eliminar

#### Response (204 No Content)

Sin contenido en el body.

#### Response (404 Not Found)

```json
{
  "detail": "Personaje no encontrado"
}
```

---

## Códigos de Estado

| Código | Descripción |
|--------|-------------|
| 200 | OK - Solicitud exitosa |
| 201 | Created - Recurso creado exitosamente |
| 204 | No Content - Eliminación exitosa |
| 400 | Bad Request - Datos inválidos |
| 404 | Not Found - Recurso no encontrado |
| 500 | Internal Server Error - Error en el servidor |

## Ejemplos con cURL

### Crear colección con personajes

```bash
curl -X POST "http://localhost:8000/api/v1/collections/" \
  -H "Content-Type: application/json" \
  -d '{
    "name":"Mi Colección",
    "image_url":"https://example.com/image.jpg",
    "characters": [
      {"name":"Personaje 1","image_url":"https://example.com/char1.jpg"},
      {"name":"Personaje 2","image_url":"https://example.com/char2.jpg"}
    ]
  }'
```

### Obtener colección con personajes

```bash
curl -X GET "http://localhost:8000/api/v1/collections/1"
```

### Agregar personaje a colección

```bash
curl -X POST "http://localhost:8000/api/v1/collections/1/characters" \
  -H "Content-Type: application/json" \
  -d '{"name":"Nuevo Personaje","image_url":"https://example.com/char.jpg"}'
```

### Obtener personajes de una colección

```bash
curl -X GET "http://localhost:8000/api/v1/collections/1/characters?skip=0&limit=10"
```

### Actualizar personaje

```bash
curl -X PUT "http://localhost:8000/api/v1/collections/1/characters/1" \
  -H "Content-Type: application/json" \
  -d '{"name":"Personaje Actualizado"}'
```

### Eliminar personaje

```bash
curl -X DELETE "http://localhost:8000/api/v1/collections/1/characters/1"
```
