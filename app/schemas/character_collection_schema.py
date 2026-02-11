from typing import Optional
from datetime import datetime
from pydantic import BaseModel, Field


# ============= Schemas para Character =============

class CharacterBase(BaseModel):
    """Schema base para personajes"""
    name: str = Field(..., min_length=1, max_length=255, description="Nombre del personaje")
    image_url: Optional[str] = Field(None, description="URL de la imagen del personaje")


class CharacterCreate(CharacterBase):
    """Schema para crear un nuevo personaje"""
    pass


class CharacterUpdate(BaseModel):
    """Schema para actualizar un personaje"""
    name: Optional[str] = Field(None, min_length=1, max_length=255, description="Nombre del personaje")
    image_url: Optional[str] = Field(None, description="URL de la imagen del personaje")


class CharacterResponse(CharacterBase):
    """Schema de respuesta para un personaje"""
    id: int = Field(..., description="ID único del personaje")
    collection_id: int = Field(..., description="ID de la colección a la que pertenece")
    created_at: datetime = Field(..., description="Fecha de creación")
    updated_at: datetime = Field(..., description="Fecha de última actualización")

    class Config:
        from_attributes = True


# ============= Schemas para CharacterCollection =============

class CharacterCollectionBase(BaseModel):
    """Schema base para colecciones de personajes"""
    name: str = Field(..., min_length=1, max_length=255, description="Nombre de la colección")
    image_url: Optional[str] = Field(None, description="URL de la imagen de la colección")


class CharacterCollectionCreate(CharacterCollectionBase):
    """Schema para crear una nueva colección"""
    characters: Optional[list[CharacterCreate]] = Field(
        None,
        description="Lista de personajes iniciales (opcional)"
    )


class CharacterCollectionUpdate(BaseModel):
    """Schema para actualizar una colección"""
    name: Optional[str] = Field(None, min_length=1, max_length=255, description="Nombre de la colección")
    image_url: Optional[str] = Field(None, description="URL de la imagen de la colección")


class CharacterCollectionResponse(CharacterCollectionBase):
    """Schema de respuesta para una colección (sin characters)"""
    id: int = Field(..., description="ID único de la colección")
    created_at: datetime = Field(..., description="Fecha de creación")
    updated_at: datetime = Field(..., description="Fecha de última actualización")

    class Config:
        from_attributes = True


class CharacterCollectionWithCharactersResponse(CharacterCollectionBase):
    """Schema de respuesta para una colección con sus personajes"""
    id: int = Field(..., description="ID único de la colección")
    characters: list[CharacterResponse] = Field(..., description="Lista de personajes en la colección")
    created_at: datetime = Field(..., description="Fecha de creación")
    updated_at: datetime = Field(..., description="Fecha de última actualización")

    class Config:
        from_attributes = True


class CharacterCollectionListResponse(BaseModel):
    """Schema para listado de colecciones"""
    total: int = Field(..., description="Total de colecciones")
    skip: int = Field(..., description="Número de elementos saltados")
    limit: int = Field(..., description="Límite de elementos")
    items: list[CharacterCollectionResponse] = Field(..., description="Lista de colecciones")


class CharacterListResponse(BaseModel):
    """Schema para listado de personajes"""
    total: int = Field(..., description="Total de personajes")
    skip: int = Field(..., description="Número de elementos saltados")
    limit: int = Field(..., description="Límite de elementos")
    items: list[CharacterResponse] = Field(..., description="Lista de personajes")
