# =============================================================================
# ETAPA 6 — Cupones periódicos y TIRE con búsqueda numérica
# =============================================================================
#
# ¿Por qué ya no se puede despejar r a mano?
# Con un solo pago, la ecuación P = (C+A)/(1+r)^t tiene una sola incógnita
# y una potencia: se despeja con un poco de álgebra (lo que ya hiciste).
# Con VARIOS pagos, r aparece elevado a distintas potencias en cada término
# de la suma (t1, t2, t3...) — no hay forma de "despejar r" con operaciones
# algebraicas normales. Es un polinomio de grado alto, básicamente.
#
# La solución: en vez de DESPEJAR, ADIVINAMOS y corregimos. La idea:
#   1. Definimos una función f(r) = (valor presente de todos los pagos,
#      usando esa tasa r) - (precio que pagaste hoy)
#   2. Buscamos qué r hace que f(r) = 0 -- ese r ES la TIRE, por
#      definición (retomá la fórmula de tu docx: la TIRE es la tasa que
#      iguala precio con valor presente de los flujos).
#   3. Un algoritmo numérico prueba valores de r, mirando si f(r) da
#      positivo o negativo, y va acotando el rango hasta encontrar
#      (con muchísima precisión) el r donde f(r) cruza el cero.
#
# Nosotros no escribimos ese algoritmo de búsqueda a mano: usamos
# `scipy.optimize.brentq`, que lo hace por vos. Le pasás:
#   - la función f(r)
#   - un rango [a, b] donde f cambia de signo (ahí "sabe" que el cero
#     está adentro)
# y te devuelve el r que hace f(r) = 0.
#
# -----------------------------------------------------------------------
# TU TAREA — 2 funciones para completar
# -----------------------------------------------------------------------

from dataclasses import dataclass
from datetime import date

from dateutil.relativedelta import relativedelta
from scipy.optimize import brentq

from app.models import FrecuenciaPago, ObligacionNegociable

MESES_POR_FRECUENCIA = {
    FrecuenciaPago.MENSUAL: 1,
    FrecuenciaPago.TRIMESTRAL: 3,
    FrecuenciaPago.SEMESTRAL: 6,
}


@dataclass
class Pago:
    fecha: date
    cupon: float
    amortizacion: float

    @property
    def total(self) -> float:
        return self.cupon + self.amortizacion


def generar_flujo_de_fondos(on: ObligacionNegociable, desde: date | None = None) -> list[Pago]:
    """Genera la lista de pagos futuros de la ON, desde `desde` (default hoy)
    hasta el vencimiento"""
    desde = desde or date.today()

    # Caso todo se paga al finalizar
    if on.frecuencia_pago == FrecuenciaPago.AL_FINALIZAR:
        años = (on.fecha_vencimiento - desde).days / 365
        cupon = on.monto_nominal * (on.tasa_nominal_anual / 100) * años
        return [Pago(fecha=on.fecha_vencimiento, cupon=cupon, amortizacion=on.monto_nominal)]

    # Caso se paga por mes
    meses = MESES_POR_FRECUENCIA[on.frecuencia_pago]
    cupon_por_pago = on.monto_nominal * (on.tasa_nominal_anual/100) * (meses/12)
    
    # fechas de pago
    fechas = []
    cursor = on.fecha_vencimiento
    while cursor >= desde:
        fechas.append(cursor)
        cursor = cursor - relativedelta(months=meses)
    fechas.sort()
    
    pagos = []
    for indice, fecha in enumerate(fechas):
        if(indice == len(fechas)-1):
            pagos.append(Pago(fecha, cupon_por_pago, on.monto_nominal))
        else:
            pagos.append(Pago(fecha, cupon_por_pago, 0))
        
    return pagos


def calcular_tire(on: ObligacionNegociable, precio_mercado_pct: float, desde: date | None = None) -> float:
    """Calcula la TIRE (en %) buscando numéricamente la tasa r que hace que
    el valor presente del flujo de fondos sea igual al precio de mercado"""
    desde = desde or date.today()
    flujo = generar_flujo_de_fondos(on, desde=desde)
    precio_en_dolares = on.monto_nominal * (precio_mercado_pct / 100)

    if precio_en_dolares <= 0:
        raise ValueError("precio_mercado_pct debe ser mayor que 0")
    if not flujo:
        raise ValueError("no hay pagos futuros para esta ON")

    def valor_presente_neto(r):
        valor_presente_total = 0
        for pago in flujo:
            t_anios = (pago.fecha - desde).days / 365
            valor_presente_total += pago.total/(1+r)**t_anios
        return(valor_presente_total-precio_en_dolares)

    r = brentq(valor_presente_neto, -0.5, 2.0) # TIRE entre -50% y +200% anual
    
    return round(r*100, 2)