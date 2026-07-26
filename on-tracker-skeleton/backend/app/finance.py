from datetime import date

from app.models import ObligacionNegociable


def calcular_pago_al_vencimiento(on: ObligacionNegociable) -> tuple[float, float, float]:
    """Devuelve (cupon, amortizacion, años) para un bono que paga todo
    junto al vencimiento"""
    
    dias = (on.fecha_vencimiento - date.today()).days
    años = dias / 365

    cupon = on.monto_nominal * (on.tasa_nominal_anual/100) * años
    
    return (cupon, on.monto_nominal, años) # amortización = monto_nominal porque se devuelve todo al final
    


def calcular_tire(on: ObligacionNegociable, precio_mercado_pct: float) -> float:
    """Calcula la TIRE (en %) a partir del precio de mercado (% de la par)"""
    cupon, amortizacion, años = calcular_pago_al_vencimiento(on)

    precio_en_dolares = on.monto_nominal * (precio_mercado_pct/100)

    if precio_en_dolares <= 0:
        raise ValueError("precio_mercado_pct debe ser mayor que 0")
    if años <= 0:
        raise ValueError("fecha_vencimiento debe ser una fecha futura")

    total_pago = cupon + amortizacion

    r = (total_pago / precio_en_dolares) ** (1 / años) - 1

    return round(r * 100, 2)