from abc import ABC, abstractmethod
from typing import List, Optional
from app.models.character import Character


class ICharacterRepository(ABC):
    """Interfaz del repositorio de personajes"""

    @abstractmethod
    def create(self, character: Character) -> Character:
        """Crear un nuevo personaje"""
        pass

    @abstractmethod
    def read(self, character_id: int) -> Optional[Character]:
        """Obtener un personaje por ID"""
        pass

    @abstractmethod
    def read_by_collection(self, collection_id: int, skip: int = 0, limit: int = 100) -> List[Character]:
        """Obtener todos los personajes de una colección"""
        pass

    @abstractmethod
    def update(self, character_id: int, character: Character) -> Optional[Character]:
        """Actualizar un personaje existente"""
        pass

    @abstractmethod
    def delete(self, character_id: int) -> bool:
        """Eliminar un personaje"""
        pass

    @abstractmethod
    def delete_by_collection(self, collection_id: int) -> int:
        """Eliminar todos los personajes de una colección"""
        pass

    @abstractmethod
    def exists(self, character_id: int) -> bool:
        """Verificar si existe un personaje"""
        pass
