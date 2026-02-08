# Documentación de API - Impostor

Bienvenido a la documentación de la API del proyecto **Impostor**.

## 📋 Estructura

Esta documentación está organizada por tipos de endpoint:

### WebSocket API

- **[Endpoints WebSocket](./websocket/endpoints.md)** - Documentación detallada de todos los endpoints WebSocket
  - Descripción de endpoints `/ws/{room_id}` y `/ws`
  - Formatos de mensajes esperados y respuestas
  - Ejemplos de uso en JavaScript, Python, Node.js y cURL

### HTTP API (Futuro)

- HTTP API (próximamente si se requiere)

## 🚀 Inicio Rápido

### Instalación de dependencias

```bash
pip install -r requirements.txt
```

### Ejecutar el servidor

```bash
python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

### Conectarse a una sala WebSocket

1. Crear una sala (POST `/rooms`) para obtener un `room_id`.

```bash
curl -s -X POST http://127.0.0.1:8000/rooms | jq
# => { "room_id": "abc12345" }
```

2. Conectarse a la sala usando `room_id`:

```javascript
const roomId = 'abc12345';
const playerName = 'Juan';
const ws = new WebSocket(`ws://localhost:8000/ws/${roomId}?player_name=${playerName}`);

ws.onmessage = (event) => {
  console.log(JSON.parse(event.data));
};
```

Para más ejemplos y detalles, consulta la [documentación de WebSocket](./websocket/endpoints.md).

## 📝 Información General

- **Nombre del proyecto:** Impostor
- **Versión:** 1.0.0
- **Descripción:** Juego de roles en tiempo real con WebSocket para múltiples salas
- **Protocolo principal:** WebSocket (RFC 6455)

## 🔗 Enlaces Útiles

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [WebSocket RFC 6455](https://tools.ietf.org/html/rfc6455)
- [JSON Specification](https://www.json.org/)

## 📞 Soporte

Para reportar issues o sugerencias, consulta el repositorio del proyecto.
