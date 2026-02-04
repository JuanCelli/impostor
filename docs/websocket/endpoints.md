# WebSocket API Endpoints

Documentación de todos los endpoints WebSocket disponibles en la API Impostor.

## Tabla de contenidos

- [Información General](#información-general)
- [Endpoint: `/ws/{room_id}`](#endpoint-wsroom_id)
- [Endpoint: `/ws`](#endpoint-ws)
- [Mensajes Esperados](#mensajes-esperados)
- [Mensajes de Respuesta](#mensajes-de-respuesta)
- [Ejemplos de Uso](#ejemplos-de-uso)

---

## Información General

**Versión API:** 1.0.0  
**Descripción:** Juego de roles en tiempo real con WebSocket para múltiples salas  
**Protocolo:** WebSocket (RFC 6455)  
**Formato de datos:** JSON

### Autenticación

Actualmente no hay autenticación. El acceso es libre mediante `player_name`.

### Parámetros Comunes

- **`player_name`** (query, opcional): Nombre del jugador. Si se omite o es `null`, la conexión se rechaza.
- **`room_id`** (path, opcional): ID de la sala. Se genera automáticamente si no existe.

---

## Endpoint: `/ws/{room_id}`

Conecta a una sala existente o la crea si no existe.

### Especificación

| Propiedad | Valor |
|-----------|-------|
| **Path** | `/ws/{room_id}` |
| **Método** | WebSocket |
| **Nombre interno** | `websocket_with_room` |
| **Descripción** | Conecta a una sala específica por ID |

### Parámetros

#### Path Parameters
- **`room_id`** (string, requerido)
  - ID único de la sala
  - Si no existe, se crea automáticamente
  - Ejemplo: `abc123`, `room-001`, `game-session-1`

#### Query Parameters
- **`player_name`** (string, requerido)
  - Nombre del jugador que se conecta
  - Si se omite o es el string `"null"`, la conexión se rechaza
  - Ejemplo: `?player_name=Juan`, `?player_name=Alice`

### Ejemplo de Conexión

```
ws://localhost:8000/ws/sala-001?player_name=Juan
wss://api.example.com/ws/game-2024-01?player_name=María
```

### Mensajes Esperados desde Cliente

El cliente puede enviar mensajes JSON con las siguientes acciones:

#### Acción: `next_round`

```json
{
  "action": "next_round"
}
```

**Requerimientos:**
- Solo el administrador de la sala puede ejecutar esta acción
- La sala debe estar completa (todos los jugadores conectados)
- Se inicia una nueva ronda de juego

**Respuesta exitosa:**
- Los jugadores reciben información de la ronda actual

**Respuesta si la sala no está lista:**
- Se envía el estado de espera a todos los jugadores

---

## Endpoint: `/ws`

Crea una nueva sala automáticamente y conecta el jugador.

### Especificación

| Propiedad | Valor |
|-----------|-------|
| **Path** | `/ws` |
| **Método** | WebSocket |
| **Nombre interno** | `websocket_without_room` |
| **Descripción** | Crea una sala nueva automáticamente |

### Parámetros

#### Query Parameters
- **`player_name`** (string, requerido)
  - Nombre del jugador que se conecta
  - Si se omite o es el string `"null"`, la conexión se rechaza
  - Ejemplo: `?player_name=Carlos`, `?player_name=Sophia`

### Ejemplo de Conexión

```
ws://localhost:8000/ws?player_name=Carlos
wss://api.example.com/ws?player_name=Sophia
```

### Comportamiento

1. Se genera automáticamente un ID único para la nueva sala (formato: `8 caracteres aleatorios`)
2. El primer jugador que se conecta se convierte en **administrador** de la sala
3. Se asignan personajes disponibles a los jugadores según la cuota configurada (actualmente 2 jugadores)
4. Se envía el estado inicial de la sala a todos los jugadores conectados

### Mensajes Esperados desde Cliente

Igual que el endpoint `/ws/{room_id}`. Ver sección [Mensajes Esperados](#mensajes-esperados).

---

## Mensajes Esperados

### Estructura General

```json
{
  "action": "string",
  "data": {}
}
```

### Acciones Disponibles

#### 1. Siguiente Ronda (`next_round`)

**Descripción:** Inicia la siguiente ronda de juego.

**Requisitos:**
- Solo el administrador puede ejecutar
- Todos los jugadores de la sala deben estar conectados
- La sala debe estar en estado "espera" (waiting_state)

**Formato:**
```json
{
  "action": "next_round"
}
```

**Respuesta en caso de éxito:**
- Todos los jugadores reciben información de la nueva ronda
- Se asignan roles (impostor y civiles)

**Respuesta si hay error:**
- Se envía el estado actual de la sala (waiting_state)

---

## Mensajes de Respuesta

Los mensajes enviados por el servidor al cliente tienen un código y contenido específicos.

### Código 1: Estado de Espera (`waiting_state`)

Se envía cuando la sala está esperando que más jugadores se conecten o cuando la ronda aún no ha comenzado.

**Estructura esperada:**
```json
{
  "status": "waiting",
  "room_id": "abc12345",
  "players": ["Juan", "María"],
  "total_players": 2,
  "required_players": 2
}
```

### Código 2: Información de Ronda

Se envía cuando comienza una nueva ronda. Contiene información específica del jugador y del estado del juego.

**Estructura esperada:**
```json
{
  "status": "playing",
  "room_id": "abc12345",
  "player_id": "unique-player-id",
  "is_impostor": false,
  "characters": ["Oso", "Gato", "Perro"],
  "round_number": 1,
  "players": [
    {"name": "Juan", "alive": true},
    {"name": "María", "alive": true}
  ]
}
```

---

## Ejemplos de Uso

### Ejemplo 1: Crear una sala nueva con JavaScript

```javascript
const playerName = "Juan";
const ws = new WebSocket(`ws://localhost:8000/ws?player_name=${playerName}`);

ws.onopen = () => {
  console.log("Conectado a la sala");
};

ws.onmessage = (event) => {
  const message = JSON.parse(event.data);
  console.log("Mensaje recibido:", message);
  
  if (message.status === "waiting") {
    console.log(`Esperando ${message.required_players - message.total_players} jugador(es) más`);
  } else if (message.status === "playing") {
    if (message.is_impostor) {
      console.log("¡Eres el impostor!");
    } else {
      console.log("Eres un civil");
    }
  }
};

ws.onerror = (error) => {
  console.error("Error en WebSocket:", error);
};
```

### Ejemplo 2: Conectarse a una sala existente con Python

```python
import asyncio
import json
import websockets

async def connect_to_room():
    room_id = "sala-001"
    player_name = "María"
    uri = f"ws://localhost:8000/ws/{room_id}?player_name={player_name}"
    
    async with websockets.connect(uri) as websocket:
        print(f"Conectado a la sala {room_id} como {player_name}")
        
        # Enviar solicitud de próxima ronda (si eres admin)
        await websocket.send(json.dumps({"action": "next_round"}))
        
        # Recibir mensajes
        while True:
            message = await websocket.recv()
            data = json.loads(message)
            print("Mensaje recibido:", data)

asyncio.run(connect_to_room())
```

### Ejemplo 3: Conectarse a una sala existente con cURL y `websocat`

```bash
# Instalar websocat: https://github.com/vi/websocat

# Conectarse a una sala
websocat ws://localhost:8000/ws/room-001?player_name=Carlos

# En el cliente interactivo, enviar:
{"action": "next_round"}
```

### Ejemplo 4: Cliente básico con Node.js

```javascript
const WebSocket = require('ws');

const playerName = "Sophia";
const roomId = "game-session-1";
const ws = new WebSocket(`ws://localhost:8000/ws/${roomId}?player_name=${playerName}`);

ws.on('open', () => {
  console.log(`${playerName} conectado a la sala ${roomId}`);
});

ws.on('message', (data) => {
  try {
    const message = JSON.parse(data);
    console.log('Estado:', message.status);
    console.log('Datos:', JSON.stringify(message, null, 2));
  } catch (e) {
    console.error('Error parseando mensaje:', e);
  }
});

ws.on('close', () => {
  console.log('Desconectado de la sala');
});

ws.on('error', (error) => {
  console.error('Error WebSocket:', error);
});
```

---

## Notas y Consideraciones

### Limitaciones Actuales

- **Sin autenticación:** Cualquiera puede conectarse usando un nombre
- **Cuota fija:** Actualmente configurada para máximo 2 jugadores por sala
- **Sin persistencia:** Las salas desaparecen cuando se desconectan todos los jugadores
- **Sin reconexión:** Si se pierde la conexión, debe reconectarse a una nueva sala

### Comportamiento de Desconexión

- Cuando un jugador se desconecta, se envía el estado actualizado a los jugadores restantes
- Si una sala queda vacía, se elimina automáticamente

### Límites

- **Tamaño máximo de mensaje:** No especificado (ver configuración de Uvicorn)
- **Timeout de conexión:** Dependiente del servidor (por defecto sin timeout específico en FastAPI)
- **Número máximo de conexiones simultáneas:** Limitado solo por recursos del servidor

---

## Versiones Futuras

Esta documentación será actualizada cuando se añadan nuevos endpoints o se modifiquen los existentes.
