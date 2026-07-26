from sqlmodel import Session, SQLModel, create_engine

engine = create_engine("sqlite:///./on_tracker.db")


def crear_tablas() -> None:
    '''crea las tablas de todas las clases definidas con table=True'''
    SQLModel.metadata.create_all(engine)


def get_session():
    """Generador que abre una Session, se la 'presta' al endpoint que la
    pida, y la cierra sola cuando el pedido HTTP termina.
    """
    # Yield para que no se corte la session de una, sino que espera a que lo pidan (con next)
    with Session(engine) as session:
        yield session
        