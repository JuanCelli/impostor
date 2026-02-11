from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.config.database import Base


class CharacterCollectionModel(Base):
    """Modelo SQLAlchemy de la tabla character_collections"""
    
    __tablename__ = "character_collections"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, index=True)
    image_url = Column(Text, nullable=True)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)

    # Relación one-to-many con characters
    characters = relationship(
        "CharacterModel",
        back_populates="collection",
        cascade="all, delete-orphan",
        lazy="joined"
    )

    def __repr__(self):
        return f"<CharacterCollectionModel(id={self.id}, name='{self.name}', characters_count={len(self.characters)})>"


class CharacterModel(Base):
    """Modelo SQLAlchemy de la tabla characters"""
    
    __tablename__ = "characters"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, index=True)
    image_url = Column(Text, nullable=True)
    collection_id = Column(Integer, ForeignKey("character_collections.id"), nullable=False, index=True)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)

    # Relación many-to-one con collection
    collection = relationship("CharacterCollectionModel", back_populates="characters")

    def __repr__(self):
        return f"<CharacterModel(id={self.id}, name='{self.name}', collection_id={self.collection_id})>"
