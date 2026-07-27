from collections import defaultdict
from datetime import date, timedelta

from fastapi import APIRouter, Depends
from sqlmodel import Session, select

from app.database import get_session
from app.finance import generar_flujo_de_fondos
from app.models import ObligacionNegociable

router = APIRouter(prefix="/dashboard", tags=["dashboard"])


@router.get("/resumen")
def resumen(session: Session = Depends(get_session)):
    ons = session.exec(select(ObligacionNegociable)).all()

    total_invertido = sum(on.monto_nominal for on in ons)
    por_banco = defaultdict(float)
    por_empresa = defaultdict(float)
    intereses_proximos_12_meses = 0
    
    for on in ons:
        por_banco[on.banco] += on.monto_nominal
        por_empresa[on.empresa] += on.monto_nominal
        limite = date.today() + timedelta(days=365)
        for pago in generar_flujo_de_fondos(on):
            if pago.fecha <= limite:
                intereses_proximos_12_meses += pago.cupon
    
    

    return {
        "total_invertido": total_invertido,
        "intereses_proximos_12_meses": intereses_proximos_12_meses,
        "cantidad_ons": len(ons),
        "por_banco": por_banco,
        "por_empresa": por_empresa,
    }


@router.get("/calendario-pagos")
def calendario_pagos(session: Session = Depends(get_session)):
    """Todos los pagos futuros de todas las ONs, ordenados por fecha --
    ya armado entero, no hace falta tocar nada acá. Es el mismo patrón
    que ya usaste, solo que "aplanando" varias listas en una."""
    ons = session.exec(select(ObligacionNegociable)).all()
    eventos = []
    for on in ons:
        for pago in generar_flujo_de_fondos(on):
            eventos.append({
                "fecha": pago.fecha,
                "on_id": on.id,
                "ticker": on.ticker,
                "empresa": on.empresa,
                "cupon": pago.cupon,
                "amortizacion": pago.amortizacion,
            })
    eventos.sort(key=lambda e: e["fecha"])
    return eventos