import pytest
from sqlmodel import Session, SQLModel, create_engine
from sqlalchemy.pool import StaticPool

from app.models import ObligacionNegociable


@pytest.fixture
def session():
    # Engine en memoria para no usar archivos externos (StaticPool para que todas las conexiones usen la misma base en memoria y no tire error)
    test_engine = create_engine("sqlite:///:memory:", poolclass=StaticPool, connect_args={"check_same_thread": False})

    SQLModel.metadata.create_all(test_engine)

    with Session(test_engine) as session:
        # yield así se cierra la sesion cuando termina de correrse el test
        yield session