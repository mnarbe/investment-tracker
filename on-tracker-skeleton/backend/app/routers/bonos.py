from fastapi import APIRouter, Depends
from sqlmodel import Session, select

from app.database import get_session
from app.finance import calcular_tire
from app.models import ObligacionNegociable

router = APIRouter(prefix="/bonos", tags=["bonos"])


@router.get("", response_model=list) # la response es un dict con la ON y el TIRE calculado
def listar_bonos(session: Session = Depends(get_session)):
    
    ons = session.exec(select(ObligacionNegociable)).all()
    resultado = []
    
    for on in ons:
        datos = on.model_dump()
        if on.precio_compra_mercado_secundario is not None:
            datos["tire_actual"] = calcular_tire(on, on.precio_compra_mercado_secundario)
        else:
            datos["tire_actual"] = None
        resultado.append(datos)
    
    return resultado