from dataclasses import dataclass
from datetime import date

from dateutil.relativedelta import relativedelta

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
    hasta el vencimiento."""
    desde = desde or date.today()
    if on.fecha_inicio and on.fecha_inicio > desde:
        desde = on.fecha_inicio

    # Caso todo se paga al finalizar
    if on.frecuencia_pago == FrecuenciaPago.AL_FINALIZAR:
        años = (on.fecha_vencimiento - desde).days / 365
        cupon = on.monto_nominal * (on.tasa_nominal_anual / 100) * años
        return [Pago(fecha=on.fecha_vencimiento, cupon=cupon, amortizacion=on.monto_nominal)]

    # Caso se paga por frecuencia periódica
    meses = MESES_POR_FRECUENCIA[on.frecuencia_pago]
    cupon_por_pago = on.monto_nominal * (on.tasa_nominal_anual / 100) * (meses / 12)

    fechas = []
    cursor = on.fecha_vencimiento
    while cursor >= desde:
        fechas.append(cursor)
        cursor = cursor - relativedelta(months=meses)
    fechas.sort()

    pagos = []
    for indice, fecha in enumerate(fechas):
        if indice == len(fechas) - 1:
            pagos.append(Pago(fecha, cupon_por_pago, on.monto_nominal))
        else:
            pagos.append(Pago(fecha, cupon_por_pago, 0))

    return pagos