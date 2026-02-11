import logging
from typing import List, Optional

from app.models.character_collection import CharacterCollection
from app.models.character import Character
from app.repositories.character_collection_repository import ICharacterCollectionRepository
from app.repositories.character_repository import ICharacterRepository

logger = logging.getLogger(__name__)


class CharacterCollectionService:
    """Servicio de negocio para gestionar colecciones de personajes"""

    def __init__(
        self,
        collection_repository: ICharacterCollectionRepository,
        character_repository: Optional[ICharacterRepository] = None
    ):
        self.collection_repository = collection_repository
        self.character_repository = character_repository

    def create_collection(
        self,
        name: str,
        image_url: Optional[str] = None,
        characters: Optional[List[dict]] = None
    ) -> CharacterCollection:
        """Crear una nueva colección con caracteres opcionales"""
        if not name or not name.strip():
            raise ValueError("El nombre de la colección no puede estar vacío")
        
        collection = CharacterCollection(
            name=name.strip(),
            image_url=image_url,
            characters=[]
        )
        
        created = self.collection_repository.create(collection)
        
        # Agregar characters si se proporcionan
        if characters and self.character_repository:
            for char_data in characters:
                try:
                    character = Character(
                        name=char_data.get("name"),
                        image_url=char_data.get("image_url"),
                        collection_id=created.id
                    )
                    created_char = self.character_repository.create(character)
                    created.add_character(created_char)
                    logger.info(f"Personaje '{created_char.name}' agregado a colección {created.id}")
                except Exception as e:
                    logger.warning(f"Error al agregar personaje a colección: {e}")
        
        logger.info(f"Colección creada: {created.id} - {created.name}")
        return created

    def get_collection(self, collection_id: int) -> Optional[CharacterCollection]:
        """Obtener una colección por ID"""
        if collection_id <= 0:
            raise ValueError("El ID debe ser un número positivo")
        
        return self.collection_repository.read(collection_id)

    def get_all_collections(self, skip: int = 0, limit: int = 100) -> List[CharacterCollection]:
        """Obtener todas las colecciones con paginación"""
        if skip < 0 or limit <= 0:
            raise ValueError("skip debe ser >= 0 y limit debe ser > 0")
        
        return self.collection_repository.read_all(skip=skip, limit=limit)

    def update_collection(
        self,
        collection_id: int,
        name: Optional[str] = None,
        image_url: Optional[str] = None
    ) -> Optional[CharacterCollection]:
        """Actualizar una colección existente"""
        if collection_id <= 0:
            raise ValueError("El ID debe ser un número positivo")
        
        # Verificar que colección existe
        existing = self.collection_repository.read(collection_id)
        if not existing:
            return None
        
        # Mantener valores existentes si no se proporciona nuevos
        updated_name = name if name is not None else existing.name
        updated_image_url = image_url if image_url is not None else existing.image_url
        
        # Validar que el nombre no esté vacío
        if not updated_name or not updated_name.strip():
            raise ValueError("El nombre de la colección no puede estar vacío")
        
        collection = CharacterCollection(
            id=collection_id,
            name=updated_name.strip(),
            image_url=updated_image_url,
            characters=existing.characters
        )
        
        updated = self.collection_repository.update(collection_id, collection)
        logger.info(f"Colección actualizada: {collection_id}")
        return updated

    def delete_collection(self, collection_id: int) -> bool:
        """Eliminar una colección"""
        if collection_id <= 0:
            raise ValueError("El ID debe ser un número positivo")
        
        deleted = self.collection_repository.delete(collection_id)
        if deleted:
            logger.info(f"Colección eliminada: {collection_id}")
        return deleted

    def collection_exists(self, collection_id: int) -> bool:
        """Verificar si una colección existe"""
        return self.collection_repository.exists(collection_id)

    # ============= Métodos para gestionar characters =============

    def add_character(
        self,
        collection_id: int,
        name: str,
        image_url: Optional[str] = None
    ) -> Optional[Character]:
        """Agregar un nuevo personaje a una colección"""
        if not self.character_repository:
            raise RuntimeError("Character repository no está disponible")
        
        if collection_id <= 0:
            raise ValueError("El ID de colección debe ser un número positivo")
        
        if not name or not name.strip():
            raise ValueError("El nombre del personaje no puede estar vacío")
        
        # Verificar que la colección existe
        collection = self.collection_repository.read(collection_id)
        if not collection:
            raise ValueError(f"Colección {collection_id} no existe")
        
        character = Character(
            name=name.strip(),
            image_url=image_url,
            collection_id=collection_id
        )
        
        created = self.character_repository.create(character)
        logger.info(f"Personaje '{created.name}' agregado a colección {collection_id}")
        return created

    def get_character(self, character_id: int) -> Optional[Character]:
        """Obtener un personaje por ID"""
        if not self.character_repository:
            raise RuntimeError("Character repository no está disponible")
        
        if character_id <= 0:
            raise ValueError("El ID debe ser un número positivo")
        
        return self.character_repository.read(character_id)

    def get_collection_characters(
        self,
        collection_id: int,
        skip: int = 0,
        limit: int = 100
    ) -> List[Character]:
        """Obtener todos los personajes de una colección"""
        if not self.character_repository:
            raise RuntimeError("Character repository no está disponible")
        
        if collection_id <= 0:
            raise ValueError("El ID de colección debe ser un número positivo")
        
        # Verificar que la colección existe
        if not self.collection_repository.exists(collection_id):
            raise ValueError(f"Colección {collection_id} no existe")
        
        return self.character_repository.read_by_collection(
            collection_id, skip=skip, limit=limit
        )

    def update_character(
        self,
        character_id: int,
        name: Optional[str] = None,
        image_url: Optional[str] = None
    ) -> Optional[Character]:
        """Actualizar un personaje existente"""
        if not self.character_repository:
            raise RuntimeError("Character repository no está disponible")
        
        if character_id <= 0:
            raise ValueError("El ID debe ser un número positivo")
        
        # Obtener el personaje existente
        existing = self.character_repository.read(character_id)
        if not existing:
            return None
        
        # Validar que nombre no esté vacío
        updated_name = name if name is not None else existing.name
        if not updated_name or not updated_name.strip():
            raise ValueError("El nombre del personaje no puede estar vacío")
        
        character = Character(
            id=character_id,
            name=updated_name.strip(),
            image_url=image_url if image_url is not None else existing.image_url,
            collection_id=existing.collection_id
        )
        
        updated = self.character_repository.update(character_id, character)
        logger.info(f"Personaje actualizado: {character_id}")
        return updated

    def delete_character(self, character_id: int) -> bool:
        """Eliminar un personaje de una colección"""
        if not self.character_repository:
            raise RuntimeError("Character repository no está disponible")
        
        if character_id <= 0:
            raise ValueError("El ID debe ser un número positivo")
        
        deleted = self.character_repository.delete(character_id)
        if deleted:
            logger.info(f"Personaje eliminado: {character_id}")
        return deleted

    def character_exists(self, character_id: int) -> bool:
        """Verificar si un personaje existe"""
        if not self.character_repository:
            raise RuntimeError("Character repository no está disponible")
        
        return self.character_repository.exists(character_id)
