import os
from pathlib import Path

from sqlmodel import Session, SQLModel, create_engine

BASE_DIR = Path(__file__).resolve().parents[1]
DEFAULT_DB_PATH = BASE_DIR / "on_tracker.db"

# os.getenv("DATABASE_URL", valor_por_defecto): busca la variable de entorno para que sirva no solo en mi computadora
DATABASE_URL = os.getenv("DATABASE_URL", f"sqlite:///{DEFAULT_DB_PATH.resolve().as_posix()}")

# connect_args solo hace falta para SQLite
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {})


def crear_tablas() -> None:
    '''crea las tablas de todas las clases definidas con table=True'''
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session