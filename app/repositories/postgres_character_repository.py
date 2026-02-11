from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
import logging

from app.models.character import Character
from app.models.character_collection_model import CharacterModel
from app.repositories.character_repository import ICharacterRepository

logger = logging.getLogger(__name__)


class PostgresCharacterRepository(ICharacterRepository):
    """Implementación concreta del repositorio de characters usando PostgreSQL"""

    def __init__(self, session: Session):
        self.session = session

    def create(self, character: Character) -> Character:
        """Crear un nuevo personaje"""
        try:
            db_character = CharacterModel(
                name=character.name,
                image_url=character.image_url,
                collection_id=character.collection_id
            )
            self.session.add(db_character)
            self.session.commit()
            self.session.refresh(db_character)
            
            return self._model_to_domain(db_character)
        except SQLAlchemyError as e:
            self.session.rollback()
            logger.error(f"Error al crear personaje: {e}")
            raise

    def read(self, character_id: int) -> Optional[Character]:
        """Obtener un personaje por ID"""
        try:
            db_character = self.session.query(CharacterModel).filter(
                CharacterModel.id == character_id
            ).first()
            
            if db_character:
                return self._model_to_domain(db_character)
            return None
        except SQLAlchemyError as e:
            logger.error(f"Error al leer personaje: {e}")
            raise

    def read_by_collection(self, collection_id: int, skip: int = 0, limit: int = 100) -> List[Character]:
        """Obtener todos los personajes de una colección"""
        try:
            db_characters = self.session.query(CharacterModel).filter(
                CharacterModel.collection_id == collection_id
            ).offset(skip).limit(limit).all()
            
            return [self._model_to_domain(char) for char in db_characters]
        except SQLAlchemyError as e:
            logger.error(f"Error al leer personajes: {e}")
            raise

    def update(self, character_id: int, character: Character) -> Optional[Character]:
        """Actualizar un personaje existente"""
        try:
            db_character = self.session.query(CharacterModel).filter(
                CharacterModel.id == character_id
            ).first()
            
            if not db_character:
                return None
            
            db_character.name = character.name
            db_character.image_url = character.image_url
            
            self.session.commit()
            self.session.refresh(db_character)
            
            return self._model_to_domain(db_character)
        except SQLAlchemyError as e:
            self.session.rollback()
            logger.error(f"Error al actualizar personaje: {e}")
            raise

    def delete(self, character_id: int) -> bool:
        """Eliminar un personaje"""
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
            logger.error(f"Error al eliminar personaje: {e}")
            raise

    def delete_by_collection(self, collection_id: int) -> int:
        """Eliminar todos los personajes de una colección"""
        try:
            deleted_count = self.session.query(CharacterModel).filter(
                CharacterModel.collection_id == collection_id
            ).delete()
            
            self.session.commit()
            return deleted_count
        except SQLAlchemyError as e:
            self.session.rollback()
            logger.error(f"Error al eliminar personajes de colección: {e}")
            raise

    def exists(self, character_id: int) -> bool:
        """Verificar si existe un personaje"""
        try:
            exists = self.session.query(CharacterModel).filter(
                CharacterModel.id == character_id
            ).first() is not None
            return exists
        except SQLAlchemyError as e:
            logger.error(f"Error al verificar existencia de personaje: {e}")
            raise

    @staticmethod
    def _model_to_domain(db_model: CharacterModel) -> Character:
        """Convierte un modelo SQLAlchemy a un modelo de dominio"""
        return Character(
            id=db_model.id,
            name=db_model.name,
            image_url=db_model.image_url,
            collection_id=db_model.collection_id,
            created_at=db_model.created_at,
            updated_at=db_model.updated_at
        )
