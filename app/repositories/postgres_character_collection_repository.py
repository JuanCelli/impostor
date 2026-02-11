from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
import logging

from app.models.character_collection import CharacterCollection
from app.models.character_collection_model import CharacterCollectionModel, CharacterModel
from app.repositories.character_collection_repository import ICharacterCollectionRepository

logger = logging.getLogger(__name__)


class PostgresCharacterCollectionRepository(ICharacterCollectionRepository):
    """Implementación concreta del repositorio usando PostgreSQL"""

    def __init__(self, session: Session):
        self.session = session

    def create(self, collection: CharacterCollection) -> CharacterCollection:
        """Crear una nueva colección"""
        try:
            db_collection = CharacterCollectionModel(
                name=collection.name,
                image_url=collection.image_url
            )
            self.session.add(db_collection)
            self.session.commit()
            self.session.refresh(db_collection)
            
            return self._model_to_domain(db_collection)
        except SQLAlchemyError as e:
            self.session.rollback()
            logger.error(f"Error al crear colección: {e}")
            raise

    def read(self, collection_id: int) -> Optional[CharacterCollection]:
        """Obtener una colección por ID"""
        try:
            db_collection = self.session.query(CharacterCollectionModel).filter(
                CharacterCollectionModel.id == collection_id
            ).first()
            
            if db_collection:
                return self._model_to_domain(db_collection)
            return None
        except SQLAlchemyError as e:
            logger.error(f"Error al leer colección: {e}")
            raise

    def read_all(self, skip: int = 0, limit: int = 100) -> List[CharacterCollection]:
        """Obtener todas las colecciones"""
        try:
            db_collections = self.session.query(CharacterCollectionModel).offset(
                skip
            ).limit(limit).all()
            
            return [self._model_to_domain(col) for col in db_collections]
        except SQLAlchemyError as e:
            logger.error(f"Error al leer colecciones: {e}")
            raise

    def update(self, collection_id: int, collection: CharacterCollection) -> Optional[CharacterCollection]:
        """Actualizar una colección existente"""
        try:
            db_collection = self.session.query(CharacterCollectionModel).filter(
                CharacterCollectionModel.id == collection_id
            ).first()
            
            if not db_collection:
                return None
            
            db_collection.name = collection.name
            db_collection.image_url = collection.image_url
            
            self.session.commit()
            self.session.refresh(db_collection)
            
            return self._model_to_domain(db_collection)
        except SQLAlchemyError as e:
            self.session.rollback()
            logger.error(f"Error al actualizar colección: {e}")
            raise

    def delete(self, collection_id: int) -> bool:
        """Eliminar una colección"""
        try:
            db_collection = self.session.query(CharacterCollectionModel).filter(
                CharacterCollectionModel.id == collection_id
            ).first()
            
            if not db_collection:
                return False
            
            self.session.delete(db_collection)
            self.session.commit()
            return True
        except SQLAlchemyError as e:
            self.session.rollback()
            logger.error(f"Error al eliminar colección: {e}")
            raise

    def exists(self, collection_id: int) -> bool:
        """Verificar si existe una colección"""
        try:
            exists = self.session.query(CharacterCollectionModel).filter(
                CharacterCollectionModel.id == collection_id
            ).first() is not None
            return exists
        except SQLAlchemyError as e:
            logger.error(f"Error al verificar existencia de colección: {e}")
            raise

    def add_character(self, collection_id: int, character_id: int) -> bool:
        """Agregar un personaje a una colección (si no existe)"""
        try:
            # Verificar que la colección existe
            db_collection = self.session.query(CharacterCollectionModel).filter(
                CharacterCollectionModel.id == collection_id
            ).first()
            
            if not db_collection:
                return False
            
            # Verificar que el personaje no está ya en la colección
            db_character = self.session.query(CharacterModel).filter(
                CharacterModel.id == character_id,
                CharacterModel.collection_id == collection_id
            ).first()
            
            if db_character:
                return False  # Ya existe
            
            # El personaje se agrega mediante la operación de crear CharacterModel
            return True
        except SQLAlchemyError as e:
            logger.error(f"Error al agregar personaje a colección: {e}")
            raise

    def remove_character(self, character_id: int) -> bool:
        """Remover un personaje de una colección"""
        try:
            db_character = self.session.query(CharacterModel).filter(
                CharacterModel.id == character_id
            ).first()
            
            if not db_character:
                return False
            
            self.session.delete(db_character)
            self.session.commit()
            return True
        except SQLAlchemyError as e:
            self.session.rollback()
            logger.error(f"Error al remover personaje de colección: {e}")
            raise

    def get_characters(self, collection_id: int, skip: int = 0, limit: int = 100) -> List:
        """Obtener todos los personajes de una colección"""
        try:
            db_characters = self.session.query(CharacterModel).filter(
                CharacterModel.collection_id == collection_id
            ).offset(skip).limit(limit).all()
            
            from app.models.character import Character
            return [
                Character(
                    id=char.id,
                    name=char.name,
                    image_url=char.image_url,
                    collection_id=char.collection_id,
                    created_at=char.created_at,
                    updated_at=char.updated_at
                )
                for char in db_characters
            ]
        except SQLAlchemyError as e:
            logger.error(f"Error al obtener personajes de colección: {e}")
            raise

    @staticmethod
    def _model_to_domain(db_model: CharacterCollectionModel) -> CharacterCollection:
        """Convierte un modelo SQLAlchemy a un modelo de dominio"""
        from app.models.character import Character
        
        characters = [
            Character(
                id=char.id,
                name=char.name,
                image_url=char.image_url,
                collection_id=char.collection_id,
                created_at=char.created_at,
                updated_at=char.updated_at
            )
            for char in db_model.characters
        ]
        
        return CharacterCollection(
            id=db_model.id,
            name=db_model.name,
            image_url=db_model.image_url,
            characters=characters,
            created_at=db_model.created_at,
            updated_at=db_model.updated_at
        )
