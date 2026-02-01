from typing import Optional

from fastapi import FastAPI, WebSocket
from pydantic import BaseModel

from app.characters.animals import characters as animals
from app.services.room_manager import RoomManager
from app.routes.websocket_routes import WebSocketRoutes


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

# Crear app FastAPI
app = FastAPI(
    title="Impostor",
    description="Juego de roles en tiempo real con WebSocket para múltiples salas",
    version="1.0.0"
)


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
    await ws_routes.handle_connection(websocket, room_id, player_name)


@app.websocket(
    "/ws",
    name="websocket_without_room"
)
async def websocket_without_room(
    websocket: WebSocket,
    player_name: Optional[str] = None
):
    await ws_routes.handle_connection(websocket, None, player_name)
