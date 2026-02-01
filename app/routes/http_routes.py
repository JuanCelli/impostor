from fastapi import Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from services.room_manager import RoomManager
from typing import Optional


class HTTPRoutes:
    """Maneja las rutas HTTP"""
    
    def __init__(self, room_manager: RoomManager):
        self.room_manager = room_manager
        self.templates = Jinja2Templates(directory="templates")
    
    def home(self, request: Request) -> HTMLResponse:
        """Retorna la página de inicio"""
        return self.templates.TemplateResponse("home.html", {"request": request})
    
    def status_room(self, room_id: Optional[str] = None) -> dict:
        """Retorna el estado de una sala específica o todas las salas"""
        if room_id:
            # Estado de una sala específica
            game_service = self.room_manager.get_room(room_id)
            if not game_service:
                return {"error": f"Sala {room_id} no existe"}
            
            players = game_service.players
            admins = [player.name for player in players if player.is_admin]
            
            return {
                "Mensaje": {
                    "room_id": room_id,
                    "players": [player.name for player in players],
                    "admins": admins
                }
            }
        else:
            # Estado de todas las salas activas
            all_rooms = {}
            for rid, game_service in self.room_manager.active_rooms.items():
                players = game_service.players
                all_rooms[rid] = {
                    "active_players": game_service.count_active_players,
                    "quota_players": game_service.quota_players,
                    "players": [player.name for player in players]
                }
            
            return {
                "Mensaje": {
                    "total_rooms": len(all_rooms),
                    "rooms": all_rooms
                }
            }

