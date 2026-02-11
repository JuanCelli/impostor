from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.config.database import get_db
from app.repositories.postgres_character_collection_repository import PostgresCharacterCollectionRepository
from app.repositories.postgres_character_repository import PostgresCharacterRepository
from app.services.character_collection_service import CharacterCollectionService
from app.schemas.character_collection_schema import (
    CharacterCollectionCreate,
    CharacterCollectionResponse,
    CharacterCollectionUpdate,
    CharacterCollectionListResponse,
    CharacterCollectionWithCharactersResponse,
    CharacterCreate,
    CharacterResponse,
    CharacterUpdate,
    CharacterListResponse
)

router = APIRouter(
    prefix="/api/v1/collections",
    tags=["Character Collections"],
    responses={404: {"description": "No encontrado"}},
)


def get_service(db: Session = Depends(get_db)) -> CharacterCollectionService:
    """Dependency para obtener el servicio de colecciones"""
    collection_repository = PostgresCharacterCollectionRepository(db)
    character_repository = PostgresCharacterRepository(db)
    return CharacterCollectionService(collection_repository, character_repository)


@router.post(
    "/",
    response_model=CharacterCollectionResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Crear una nueva colección",
    description="Crea una nueva colección de personajes con nombre e imagen opcional, y personajes iniciales opcionalmente"
)
async def create_collection(
    collection: CharacterCollectionCreate,
    service: CharacterCollectionService = Depends(get_service)
) -> CharacterCollectionResponse:
    """
    Crear una nueva colección de personajes:
    
    - **name**: Nombre de la colección (requerido)
    - **image_url**: URL de la imagen (opcional)
    - **characters**: Lista de personajes iniciales (opcional, cada uno con name e image_url)
    """
    try:
        created = service.create_collection(
            name=collection.name,
            image_url=collection.image_url,
            characters=[char.model_dump() for char in collection.characters] if collection.characters else None
        )
        return CharacterCollectionResponse.model_validate(created.to_dict())
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error al crear la colección")


@router.get(
    "/",
    response_model=CharacterCollectionListResponse,
    summary="Obtener todas las colecciones",
    description="Retorna un listado paginado de todas las colecciones"
)
async def get_collections(
    skip: int = Query(0, ge=0, description="Número de elementos a saltar"),
    limit: int = Query(100, ge=1, le=1000, description="Límite de elementos a retornar"),
    service: CharacterCollectionService = Depends(get_service)
) -> CharacterCollectionListResponse:
    """
    Obtener todas las colecciones con paginación:
    
    - **skip**: Número de elementos a saltar (default: 0)
    - **limit**: Número máximo de elementos a retornar (default: 100, máximo: 1000)
    """
    try:
        collections = service.get_all_collections(skip=skip, limit=limit)
        items = [
            CharacterCollectionResponse.model_validate(col.to_dict())
            for col in collections
        ]
        return CharacterCollectionListResponse(
            total=len(items),
            skip=skip,
            limit=limit,
            items=items
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error al obtener las colecciones")


@router.get(
    "/{collection_id}",
    response_model=CharacterCollectionWithCharactersResponse,
    summary="Obtener una colección con sus personajes",
    description="Retorna los detalles de una colección y todos sus personajes asociados"
)
async def get_collection(
    collection_id: int,
    service: CharacterCollectionService = Depends(get_service)
) -> CharacterCollectionWithCharactersResponse:
    """
    Obtener los detalles de una colección con sus personajes por su ID:
    
    - **collection_id**: ID de la colección (requerido)
    """
    try:
        collection = service.get_collection(collection_id)
        if not collection:
            raise HTTPException(status_code=404, detail="Colección no encontrada")
        
        data = collection.to_dict(include_characters=True)
        data["characters"] = [
            CharacterResponse.model_validate(char.to_dict())
            for char in collection.characters
        ]
        return CharacterCollectionWithCharactersResponse.model_validate(data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error al obtener la colección")


@router.put(
    "/{collection_id}",
    response_model=CharacterCollectionResponse,
    summary="Actualizar una colección",
    description="Actualiza una colección existente"
)
async def update_collection(
    collection_id: int,
    collection: CharacterCollectionUpdate,
    service: CharacterCollectionService = Depends(get_service)
) -> CharacterCollectionResponse:
    """
    Actualizar una colección existente:
    
    - **collection_id**: ID de la colección a actualizar (requerido)
    - **name**: Nuevo nombre (opcional)
    - **image_url**: Nueva URL de imagen (opcional)
    """
    try:
        updated = service.update_collection(
            collection_id=collection_id,
            name=collection.name,
            image_url=collection.image_url
        )
        if not updated:
            raise HTTPException(status_code=404, detail="Colección no encontrada")
        return CharacterCollectionResponse.model_validate(updated.to_dict())
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error al actualizar la colección")


@router.delete(
    "/{collection_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Eliminar una colección",
    description="Elimina una colección existente y todos sus personajes"
)
async def delete_collection(
    collection_id: int,
    service: CharacterCollectionService = Depends(get_service)
):
    """
    Eliminar una colección:
    
    - **collection_id**: ID de la colección a eliminar (requerido)
    """
    try:
        deleted = service.delete_collection(collection_id)
        if not deleted:
            raise HTTPException(status_code=404, detail="Colección no encontrada")
        return None
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error al eliminar la colección")


# ============= ENDPOINTS DE PERSONNAJES =============

@router.post(
    "/{collection_id}/characters",
    response_model=CharacterResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Agregar un personaje a una colección",
    description="Crea y agrega un nuevo personaje a una colección existente"
)
async def create_character(
    collection_id: int,
    character: CharacterCreate,
    service: CharacterCollectionService = Depends(get_service)
) -> CharacterResponse:
    """
    Agregar un nuevo personaje a una colección:
    
    - **collection_id**: ID de la colección (requerido)
    - **name**: Nombre del personaje (requerido)
    - **image_url**: URL de la imagen del personaje (opcional)
    """
    try:
        created = service.add_character(
            collection_id=collection_id,
            name=character.name,
            image_url=character.image_url
        )
        return CharacterResponse.model_validate(created.to_dict())
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except RuntimeError as e:
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error al crear el personaje")


@router.get(
    "/{collection_id}/characters",
    response_model=CharacterListResponse,
    summary="Obtener personajes de una colección",
    description="Retorna un listado paginado de todos los personajes de una colección"
)
async def get_characters(
    collection_id: int,
    skip: int = Query(0, ge=0, description="Número de elementos a saltar"),
    limit: int = Query(100, ge=1, le=1000, description="Límite de elementos a retornar"),
    service: CharacterCollectionService = Depends(get_service)
) -> CharacterListResponse:
    """
    Obtener personajes de una colección con paginación:
    
    - **collection_id**: ID de la colección (requerido)
    - **skip**: Número de elementos a saltar (default: 0)
    - **limit**: Número máximo de elementos a retornar (default: 100, máximo: 1000)
    """
    try:
        characters = service.get_collection_characters(
            collection_id=collection_id,
            skip=skip,
            limit=limit
        )
        items = [
            CharacterResponse.model_validate(char.to_dict())
            for char in characters
        ]
        return CharacterListResponse(
            total=len(items),
            skip=skip,
            limit=limit,
            items=items
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except RuntimeError as e:
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error al obtener personajes")


@router.get(
    "/{collection_id}/characters/{character_id}",
    response_model=CharacterResponse,
    summary="Obtener un personaje específico",
    description="Retorna los detalles de un personaje específico"
)
async def get_character(
    collection_id: int,
    character_id: int,
    service: CharacterCollectionService = Depends(get_service)
) -> CharacterResponse:
    """
    Obtener un personaje específico:
    
    - **collection_id**: ID de la colección (para validación)
    - **character_id**: ID del personaje (requerido)
    """
    try:
        # Verificar que la colección existe
        if not service.collection_exists(collection_id):
            raise HTTPException(status_code=404, detail="Colección no encontrada")
        
        character = service.get_character(character_id)
        if not character:
            raise HTTPException(status_code=404, detail="Personaje no encontrado")
        
        # Verificar que el personaje pertenece a la colección
        if character.collection_id != collection_id:
            raise HTTPException(status_code=404, detail="Personaje no pertenece a esta colección")
        
        return CharacterResponse.model_validate(character.to_dict())
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except RuntimeError as e:
        raise HTTPException(status_code=500, detail=str(e))
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error al obtener el personaje")


@router.put(
    "/{collection_id}/characters/{character_id}",
    response_model=CharacterResponse,
    summary="Actualizar un personaje",
    description="Actualiza un personaje existente"
)
async def update_character(
    collection_id: int,
    character_id: int,
    character_update: CharacterUpdate,
    service: CharacterCollectionService = Depends(get_service)
) -> CharacterResponse:
    """
    Actualizar un personaje existente:
    
    - **collection_id**: ID de la colección (para validación)
    - **character_id**: ID del personaje (requerido)
    - **name**: Nuevo nombre (opcional)
    - **image_url**: Nueva URL de imagen (opcional)
    """
    try:
        # Verificar que el personaje existe y pertenece a la colección
        character = service.get_character(character_id)
        if not character:
            raise HTTPException(status_code=404, detail="Personaje no encontrado")
        
        if character.collection_id != collection_id:
            raise HTTPException(status_code=404, detail="Personaje no pertenece a esta colección")
        
        updated = service.update_character(
            character_id=character_id,
            name=character_update.name,
            image_url=character_update.image_url
        )
        return CharacterResponse.model_validate(updated.to_dict())
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except RuntimeError as e:
        raise HTTPException(status_code=500, detail=str(e))
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error al actualizar el personaje")


@router.delete(
    "/{collection_id}/characters/{character_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Eliminar un personaje",
    description="Elimina un personaje de una colección"
)
async def delete_character(
    collection_id: int,
    character_id: int,
    service: CharacterCollectionService = Depends(get_service)
):
    """
    Eliminar un personaje de una colección:
    
    - **collection_id**: ID de la colección (para validación)
    - **character_id**: ID del personaje a eliminar (requerido)
    """
    try:
        # Verificar que el personaje existe y pertenece a la colección
        character = service.get_character(character_id)
        if not character:
            raise HTTPException(status_code=404, detail="Personaje no encontrado")
        
        if character.collection_id != collection_id:
            raise HTTPException(status_code=404, detail="Personaje no pertenece a esta colección")
        
        deleted = service.delete_character(character_id)
        if not deleted:
            raise HTTPException(status_code=404, detail="No se pudo eliminar el personaje")
        
        return None
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except RuntimeError as e:
        raise HTTPException(status_code=500, detail=str(e))
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error al eliminar el personaje")
