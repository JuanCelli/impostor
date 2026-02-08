from typing import Optional

from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
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


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # o ["*"] en dev
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
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


# Endpoint para crear una nueva sala (genera room_id)
@app.post("/rooms", name="create_room")
async def create_room():
    room_id, _ = room_manager.get_or_create_room(None)
    return {"room_id": room_id}
