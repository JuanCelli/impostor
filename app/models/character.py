from typing import Optional
from datetime import datetime


class Character:
    """Modelo de dominio para un Personaje dentro de una Colección"""
    
    def __init__(
        self, 
        name: str, 
        image_url: Optional[str] = None,
        id: Optional[int] = None,
        collection_id: Optional[int] = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None
    ):
        self.id = id
        self.name = name
        self.image_url = image_url
        self.collection_id = collection_id
        self.created_at = created_at
        self.updated_at = updated_at

    def to_dict(self) -> dict:
        """Convierte el modelo a un diccionario"""
        return {
            "id": self.id,
            "name": self.name,
            "image_url": self.image_url,
            "collection_id": self.collection_id,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Character":
        """Crea una instancia desde un diccionario"""
        return cls(
            id=data.get("id"),
            name=data.get("name"),
            image_url=data.get("image_url"),
            collection_id=data.get("collection_id"),
            created_at=data.get("created_at"),
            updated_at=data.get("updated_at"),
        )
