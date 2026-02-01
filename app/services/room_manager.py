import uuid
from typing import Dict, Optional

from app.services.game_service import GameService


class RoomManager:
    """Gestor centralizado de salas de juego"""
    
    def __init__(self, quota_players: int, characters: list[str]):
        self._rooms: Dict[str, GameService] = {}
        self.quota_players = quota_players
        self.characters = characters
    
    def get_or_create_room(self, room_id: Optional[str] = None) -> tuple[str, GameService]:
        """
        Obtiene una sala existente o crea una nueva.
        
        Args:
            room_id: ID de la sala. Si es None, genera una nueva.
            
        Returns:
            Tupla (room_id, GameService)
        """
        if room_id is None:
            # Generar nuevo ID de sala
            room_id = str(uuid.uuid4())[:8]
        
        if room_id not in self._rooms:
            # Crear nueva sala
            self._rooms[room_id] = GameService(
                quota_players=self.quota_players,
                characters=self.characters
            )
        
        return room_id, self._rooms[room_id]
    
    def get_room(self, room_id: str) -> Optional[GameService]:
        """Obtiene una sala existente"""
        return self._rooms.get(room_id)
    
    def room_exists(self, room_id: str) -> bool:
        """Verifica si una sala existe"""
        return room_id in self._rooms
    
    def delete_room(self, room_id: str) -> None:
        """Elimina una sala (cuando queda vacía)"""
        if room_id in self._rooms:
            game_service = self._rooms[room_id]
            if game_service.count_active_players == 0:
                del self._rooms[room_id]
    
    @property
    def active_rooms(self) -> Dict[str, GameService]:
        """Retorna todas las salas activas"""
        return self._rooms.copy()
