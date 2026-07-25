from sqlmodel import SQLModel, create_engine

# Engine en ./on_tracker.db, si no existe lo crea
engine = create_engine("sqlite:///./on_tracker.db")

def crear_tablas() -> None:
    '''crea las tablas de todas las clases definidas con table=True'''
    
    SQLModel.metadata.create_all(engine)