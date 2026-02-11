import os
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.pool import NullPool
import logging

logger = logging.getLogger(__name__)

# Obtener la URL de la base de datos de las variables de entorno
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://username:password@localhost:5432/impostor"
)

# SSL mode for NEON
if "neon" in DATABASE_URL.lower():
    # Configurar para NEON con SSL
    DATABASE_URL = DATABASE_URL.replace("postgresql://", "postgresql+psycopg2://")
    if "?sslmode" not in DATABASE_URL:
        DATABASE_URL += "?sslmode=require"

# Crear el motor de SQLAlchemy
engine = create_engine(
    DATABASE_URL,
    poolclass=NullPool,  # Importante para serverless/NEON
    echo=os.getenv("SQL_ECHO", "false").lower() == "true",
    connect_args={
        "connect_timeout": 10,
    }
)

# Session local
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base para los modelos declarativos
Base = declarative_base()


def get_db():
    """Dependency para obtener sesión de base de datos"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """Inicializa las tablas en la base de datos"""
    try:
        Base.metadata.create_all(bind=engine)
        logger.info("Base de datos inicializada correctamente")
    except Exception as e:
        logger.error(f"Error al inicializar la base de datos: {e}")
        raise
