from fastapi import FastAPI, WebSocket, Request
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from characters.animals import characters as animals
from services.room_manager import RoomManager
from routes.websocket_routes import WebSocketRoutes
from routes.http_routes import HTTPRoutes
from typing import Optional


# Modelos Pydantic para documentación
class RoomStatus(BaseModel):
    """Estado de una sala"""
    room_id: str
    players: list[str]
    admins: list[str]


class AllRoomsStatus(BaseModel):
    """Estado de todas las salas activas"""
    total_rooms: int
    rooms: dict


# Inicializar gestor de salas
room_manager = RoomManager(quota_players=2, characters=animals)
ws_routes = WebSocketRoutes(room_manager)
http_routes = HTTPRoutes(room_manager)

# Crear app FastAPI
app = FastAPI(
    title="Impostor",
    description="Juego de roles en tiempo real con WebSocket para múltiples salas",
    version="1.0.0"
)

# Rutas HTTP
@app.get(
    "/", 
    response_class=HTMLResponse,
    tags=["Web"],
    summary="Página de inicio"
)
def home(request: Request):
    """
    Retorna la página HTML de inicio del juego.
    
    Aquí el jugador puede conectarse a una sala existente o crear una nueva.
    """
    return http_routes.home(request)

@app.get(
    "/status/room",
    tags=["Estado"],
    summary="Ver estado de salas",
    responses={
        200: {"description": "Estado de sala(s)", "model": dict}
    }
)
def status_room(room_id: Optional[str] = None):
    """
    Retorna el estado de una sala específica o todas las salas activas.
    
    **Parámetros:**
    - `room_id` (opcional): ID de la sala específica. Si se omite, retorna todas.
    
    **Ejemplos:**
    - GET `/status/room` - Ver todas las salas activas
    - GET `/status/room?room_id=abc123` - Ver sala específica
    """
    return http_routes.status_room(room_id)

# Rutas WebSocket
@app.websocket(
    "/ws/{room_id}",
    name="websocket_with_room"
)
async def websocket_with_room(
    websocket: WebSocket, 
    room_id: str, 
    player_name: Optional[str] = None
):
    """
    Conecta a una sala existente o la crea si no existe.
    
    **Parámetros:**
    - `room_id` (path): ID de la sala (será creada si no existe)
    - `player_name` (query): Nombre del jugador (requerido)
    
    **Ejemplo:**
    ```
    ws://localhost:8000/ws/abc123?player_name=Juan
    ```
    
    **Mensajes esperados desde cliente:**
    ```json
    {
        "action": "next_round"
    }
    ```
    
    **Mensajes enviados al cliente:**
    - Code 1: Estado de espera (waiting_state)
    - Code 2: Información de la ronda (player info, impostor, etc)
    """
    await ws_routes.handle_connection(websocket, room_id, player_name)

@app.websocket(
    "/ws",
    name="websocket_without_room"
)
async def websocket_without_room(
    websocket: WebSocket, 
    player_name: Optional[str] = None
):
    """
    Crea una nueva sala automáticamente y conecta al jugador.
    
    **Parámetros:**
    - `player_name` (query): Nombre del jugador (requerido)
    
    **Ejemplo:**
    ```
    ws://localhost:8000/ws?player_name=Juan
    ```
    
    **Mensajes esperados desde cliente:**
    ```json
    {
        "action": "next_round"
    }
    ```
    
    **Mensajes enviados al cliente:**
    - Code 1: Estado de espera (waiting_state)
    - Code 2: Información de la ronda (player info, impostor, etc)
    """
    await ws_routes.handle_connection(websocket, None, player_name)
