from typing import Optional, List
from datetime import datetime


class CharacterCollection:
    """Modelo de dominio para una Colección de Personajes"""
    
    def __init__(
        self, 
        name: str, 
        image_url: Optional[str] = None, 
        id: Optional[int] = None,
        characters: Optional[List] = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None
    ):
        self.id = id
        self.name = name
        self.image_url = image_url
        self.characters = characters if characters is not None else []
        self.created_at = created_at
        self.updated_at = updated_at

    def add_character(self, character) -> None:
        """Agrega un personaje a la colección"""
        if character not in self.characters:
            self.characters.append(character)

    def remove_character(self, character) -> bool:
        """Remueve un personaje de la colección"""
        if character in self.characters:
            self.characters.remove(character)
            return True
        return False

    def get_character(self, character_id: int):
        """Obtiene un personaje por ID"""
        for char in self.characters:
            if char.id == character_id:
                return char
        return None

    def to_dict(self, include_characters: bool = False) -> dict:
        """Convierte el modelo a un diccionario"""
        data = {
            "id": self.id,
            "name": self.name,
            "image_url": self.image_url,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }
        if include_characters:
            data["characters"] = [char.to_dict() for char in self.characters]
        return data

    @classmethod
    def from_dict(cls, data: dict) -> "CharacterCollection":
        """Crea una instancia desde un diccionario"""
        return cls(
            id=data.get("id"),
            name=data.get("name"),
            image_url=data.get("image_url"),
            characters=data.get("characters", []),
            created_at=data.get("created_at"),
            updated_at=data.get("updated_at"),
        )
