from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlmodel import Session, select

from app.database import get_session
from app.finance import calcular_tire
from app.models import ObligacionNegociable

router = APIRouter(prefix="/bonos", tags=["bonos"])


class ActualizarPrecioIn(BaseModel):
    """Forma esperada del body del PATCH: {"precio_compra_mercado_secundario": 95.0}"""
    precio_compra_mercado_secundario: float


@router.get("", response_model=list)
def listar_bonos(session: Session = Depends(get_session)):
    ons = session.exec(select(ObligacionNegociable)).all()
    resultado = []
    for on in ons:
        datos = on.model_dump()
        if on.precio_compra_mercado_secundario is not None:
            try:
                datos["tire_actual"] = calcular_tire(on, on.precio_compra_mercado_secundario)
            except ValueError:
                datos["tire_actual"] = None
        else:
            datos["tire_actual"] = None
        resultado.append(datos)
    
    return resultado

@router.patch("/{on_id}/precio")
def actualizar_precio(on_id: int, payload: ActualizarPrecioIn, session: Session = Depends(get_session)):
    on = session.get(ObligacionNegociable, on_id)
    
    if on is None:
        raise HTTPException(status_code=404, detail="ON no encontrada")
    else:
        on.precio_compra_mercado_secundario = payload.precio_compra_mercado_secundario
    
    session.add(on)
    session.commit()
    session.refresh(on)
    
    datos = on.model_dump()
    try:
        datos["tire_actual"] = calcular_tire(on, on.precio_compra_mercado_secundario)
    except ValueError:
        datos["tire_actual"] = None
    
    return datos