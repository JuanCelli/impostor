import random
from typing import List, Optional, Dict, Any

from app.models.player import Player
from app.services.room_service import RoomService


class GameService:
    """Servicio de lógica de negocio para el juego"""
    
    def __init__(self, quota_players: int, characters: List[str]):
        self.room_service = RoomService()
        self.quota_players = quota_players
        self._current_character: Optional[str] = None
        self.characters = characters
    
    @property
    def players(self) -> List[Player]:
        """Retorna lista de jugadores activos"""
        return self.room_service.active_players
    
    @property
    def is_complete(self) -> bool:
        """Verifica si la sala está completa"""
        return self.room_service.count_active_players == self.quota_players
    
    @property
    def count_active_players(self) -> int:
        """Retorna cantidad de jugadores activos"""
        return self.room_service.count_active_players
    
    @property
    def current_character(self) -> Optional[str]:
        return self._current_character
    
    @current_character.setter
    def current_character(self, new_character: Optional[str]):
        self._current_character = new_character
    
    def clear_character(self):
        """Limpia el personaje actual"""
        self.current_character = None
    
    @property
    def have_admin(self) -> bool:
        """Verifica si hay admin en la sala"""
        return self.room_service.has_admin()
    
    def clear_round(self):
        """Limpia el estado de la ronda"""
        self.clear_character()
        for player in self.players:
            player.clear_state()
    
    def assign_impostor(self) -> None:
        """Asigna aleatoriamente un impostor"""
        if self.players:
            impostor_player = random.choice(self.players)
            impostor_player.set_as_impostor()
    
    def assign_first(self) -> None:
        """Asigna aleatoriamente quién empieza"""
        if self.players:
            first_player = random.choice(self.players)
            first_player.is_first = True
    
    def assign_admin(self) -> None:
        """Asigna admin si no hay ninguno"""
        if not self.players:
            return
        if not self.have_admin:
            admin_player = random.choice(self.players)
            admin_player.is_admin = True
    
    async def send_info_to_players(self) -> None:
        """Envía el estado de la ronda a todos los jugadores"""
        for player in self.players:
            data = player.info_in_round(self.current_character)
            await self.room_service.send_to_player(player, data, 2)
    
    async def new_round(self) -> None:
        """Inicia una nueva ronda"""
        self.clear_round()
        self.current_character = random.choice(self.characters)
        self.assign_impostor()
        self.assign_first()
        await self.send_info_to_players()
    
    @property
    def waiting_state(self) -> Dict[str, Any]:
        """Retorna el estado de espera de la sala"""
        return {
            "quota_players": self.quota_players,
            "active_players": self.count_active_players,
            "players": [player.info_in_room for player in self.players]
        }
    
    async def waiting(self) -> None:
        """Envía estado de espera a todos los jugadores"""
        await self.room_service.broadcast(self.waiting_state, 1)
    
    def disconnect(self, player: Player) -> None:
        """Desconecta un jugador"""
        self.room_service.disconnect(player)
        if player.is_admin:
            self.assign_admin()
    
    def connect(self, player: Player, websocket) -> bool:
        """Conecta un nuevo jugador a la sala"""
        if self.is_complete:
            print("Sala llena")
            return False
        
        connected = self.room_service.connect(player, websocket)
        if not connected:
            return False
        
        self.assign_admin()
        return True
