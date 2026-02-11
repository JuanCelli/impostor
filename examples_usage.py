"""
Ejemplo de uso del CRUD de Colecciones y Personajes

Para probar la API, ejecuta:
    uvicorn app.main:app --reload

Luego accede a:
    - Swagger UI: http://localhost:8000/docs
    - ReDoc: http://localhost:8000/redoc
"""

# ============ EJEMPLOS DE USO CON cURL ============

# 1. Crear una colección vacía
"""
curl -X POST "http://localhost:8000/api/v1/collections/" \
  -H "Content-Type: application/json" \
  -d '{"name":"Héroes"}'
"""

# 2. Crear una colección con personajes iniciales
"""
curl -X POST "http://localhost:8000/api/v1/collections/" \
  -H "Content-Type: application/json" \
  -d '{
    "name":"Villanos",
    "image_url":"https://example.com/villains.jpg",
    "characters": [
      {"name":"Joker","image_url":"https://example.com/joker.jpg"},
      {"name":"Lex Luthor","image_url":"https://example.com/lex.jpg"}
    ]
  }'
"""

# 3. Obtener todas las colecciones
"""
curl -X GET "http://localhost:8000/api/v1/collections/?skip=0&limit=10"
"""

# 4. Obtener una colección con sus personajes
"""
curl -X GET "http://localhost:8000/api/v1/collections/1"
"""

# 5. Actualizar una colección
"""
curl -X PUT "http://localhost:8000/api/v1/collections/1" \
  -H "Content-Type: application/json" \
  -d '{"name":"Villanos Actualizados"}'
"""

# 6. Agregar un personaje a una colección
"""
curl -X POST "http://localhost:8000/api/v1/collections/1/characters" \
  -H "Content-Type: application/json" \
  -d '{"name":"Thanos","image_url":"https://example.com/thanos.jpg"}'
"""

# 7. Obtener personajes de una colección
"""
curl -X GET "http://localhost:8000/api/v1/collections/1/characters?skip=0&limit=10"
"""

# 8. Obtener un personaje específico
"""
curl -X GET "http://localhost:8000/api/v1/collections/1/characters/1"
"""

# 9. Actualizar un personaje
"""
curl -X PUT "http://localhost:8000/api/v1/collections/1/characters/1" \
  -H "Content-Type: application/json" \
  -d '{"name":"Joker Actualizado"}'
"""

# 10. Eliminar un personaje
"""
curl -X DELETE "http://localhost:8000/api/v1/collections/1/characters/1"
"""

# 11. Eliminar una colección (con todos sus personajes)
"""
curl -X DELETE "http://localhost:8000/api/v1/collections/1"
"""
