from models.player import Player
from fastapi import WebSocket
from typing import List, Dict, Any, Optional


class RoomService:
    """Servicio para gestionar la sala de juego y conexiones"""
    
    def __init__(self):
        self._active_players: Dict[str, tuple[Player, WebSocket]] = {}
    
    @property
    def active_players(self) -> List[Player]:
        """Retorna lista de jugadores activos"""
        return [player for player, _ in self._active_players.values()]
    
    @property
    def count_active_players(self) -> int:
        """Retorna cantidad de jugadores activos"""
        return len(self._active_players)
    
    def get_player_websocket(self, player: Player) -> Optional[WebSocket]:
        """Obtiene el WebSocket de un jugador"""
        if player.name in self._active_players:
            _, websocket = self._active_players[player.name]
            return websocket
        return None
    
    def connect(self, player: Player, websocket: WebSocket) -> bool:
        """Conecta un nuevo jugador a la sala"""
        if player.name in self._active_players:
            return False
        self._active_players[player.name] = (player, websocket)
        return True
    
    def disconnect(self, player: Player) -> None:
        """Desconecta un jugador de la sala"""
        if player.name in self._active_players:
            del self._active_players[player.name]
    
    async def broadcast(self, data: Dict[str, Any], code_ws: int) -> None:
        """Envía un mensaje a todos los jugadores conectados"""
        data_ws = {
            "code_ws": code_ws,
            "data": data
        }
        
        for player, websocket in self._active_players.values():
            try:
                await websocket.send_json(data_ws)
            except Exception as e:
                print(f"Error broadcasting to {player.name}: {e}")
    
    async def send_to_player(self, player: Player, data: Dict[str, Any], code_ws: int) -> None:
        """Envía un mensaje a un jugador específico"""
        websocket = self.get_player_websocket(player)
        if websocket:
            data_ws = {
                "code_ws": code_ws,
                "data": data
            }
            try:
                await websocket.send_json(data_ws)
            except Exception as e:
                print(f"Error sending to {player.name}: {e}")
    
    def has_admin(self) -> bool:
        """Verifica si hay algún admin en la sala"""
        return any(player.is_admin for player in self.active_players)
