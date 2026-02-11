from abc import ABC, abstractmethod
from typing import List, Optional
from app.models.character_collection import CharacterCollection


class ICharacterCollectionRepository(ABC):
    """Interfaz del repositorio de colecciones de personajes"""

    @abstractmethod
    def create(self, collection: CharacterCollection) -> CharacterCollection:
        """Crear una nueva colección"""
        pass

    @abstractmethod
    def read(self, collection_id: int) -> Optional[CharacterCollection]:
        """Obtener una colección por ID"""
        pass

    @abstractmethod
    def read_all(self, skip: int = 0, limit: int = 100) -> List[CharacterCollection]:
        """Obtener todas las colecciones"""
        pass

    @abstractmethod
    def update(self, collection_id: int, collection: CharacterCollection) -> Optional[CharacterCollection]:
        """Actualizar una colección existente"""
        pass

    @abstractmethod
    def delete(self, collection_id: int) -> bool:
        """Eliminar una colección"""
        pass

    @abstractmethod
    def exists(self, collection_id: int) -> bool:
        """Verificar si existe una colección"""
        pass
