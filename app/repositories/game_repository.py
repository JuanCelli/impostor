from utils.storage import load_state, save_state
from typing import Dict, Any


class GameRepository:
    """Capa de acceso a datos para el estado del juego"""
    
    @staticmethod
    def get_game_state() -> Dict[str, Any]:
        """Carga el estado actual del juego desde db.json"""
        return load_state()
    
    @staticmethod
    def save_game_state(state: Dict[str, Any]) -> None:
        """Guarda el estado del juego en db.json"""
        save_state(state)
    
    @staticmethod
    def reset_game_state() -> None:
        """Resetea el estado del juego a valores iniciales"""
        initial_state = {
            "count": 0,
            "impostor_assigned": False,
            "character": None,
            "first_assigned": False
        }
        save_state(initial_state)
