from typing import Optional

from fastapi import WebSocket, WebSocketDisconnect, Query

from app.models.player import Player
from app.services.room_manager import RoomManager


class WebSocketRoutes:
    """Maneja las rutas de WebSocket"""
    
    def __init__(self, room_manager: RoomManager):
        self.room_manager = room_manager
    
    async def handle_connection(
        self,
        websocket: WebSocket,
        room_id: str,
        player_name: Optional[str] = Query(None)
    ) -> None:
        """
        Maneja la conexión de un jugador por WebSocket.
        
        Args:
            websocket: Conexión WebSocket
            room_id: ID de la sala (opcional, genera una nueva si no existe)
            player_name: Nombre del jugador (requerido)
        """
        
        # Validar nombre del jugador
        if not player_name or player_name == "null":
            return None
        
        # Obtener sala existente
        game_service = self.room_manager.get_room(room_id)
        if game_service is None:
            # Sala inexistente: cerrar conexión
            try:
                await websocket.close()
            except:
                pass
            return None
        
        # Crear jugador
        player = Player(player_name)
        connection_success = game_service.connect(player, websocket)
        
        if not connection_success:
            return None
        
        try:
            await websocket.accept()
        except:
            game_service.disconnect(player)
            self.room_manager.delete_room(room_id)
            return None
        
        try:
            # Enviar info de la sala al conectarse
            await game_service.waiting()
            
            while True:
                data = await websocket.receive_json()
                print(f"[Sala {room_id}] Datos recibidos: {data}")
                
                if player.is_admin and data.get("action") == "next_round":
                    if game_service.is_complete:
                        print(f"[Sala {room_id}] Ejecutando nueva ronda")
                        await game_service.new_round()
                    else:
                        await game_service.waiting()
        
        except WebSocketDisconnect:
            print(f"[Sala {room_id}] SE DESCONECTO PLAYER: {player.name}")
            game_service.disconnect(player)
            await game_service.waiting()
            
            # Eliminar sala si está vacía
            self.room_manager.delete_room(room_id)
            return None

