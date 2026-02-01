from typing import Optional


class Player:
    """Modelo de entidad Player sin dependencias de WebSocket"""
    
    def __init__(self, name: str):
        self.name = name
        self._role = "normal"
        self._is_first = False
        self._is_admin = False

    @property
    def is_admin(self) -> bool:
        return self._is_admin

    @is_admin.setter
    def is_admin(self, value: bool):
        self._is_admin = value

    @property
    def role(self) -> str:
        return self._role
    
    @role.setter
    def role(self, new_role: str):
        self._role = new_role

    @property
    def is_first(self) -> bool:
        return self._is_first
    
    @is_first.setter
    def is_first(self, value: bool):
        self._is_first = value

    def set_as_impostor(self):
        self.role = "impostor"

    def clear_role(self):
        self.role = "normal"

    def clear_first(self):
        self.is_first = False

    def clear_state(self):
        self.clear_first()
        self.clear_role()

    @property
    def is_impostor(self) -> bool:
        return self.role == "impostor"
    
    @property
    def info_in_room(self) -> dict:
        return {
            "name": self.name,
            "is_admin": self.is_admin
        }
    
    def info_in_round(self, character: Optional[str]) -> dict:
        return {
            "name": self.name,
            "character": character if not self.is_impostor else None,
            "is_impostor": self.is_impostor,
            "is_first": self.is_first,
            "is_admin": self.is_admin
        }
