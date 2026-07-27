from datetime import date
from enum import Enum
from typing import Optional

from sqlmodel import Field, SQLModel


class FrecuenciaPago(str, Enum):
    """Un Enum ("enumeración") restringe un campo a un set fijo de valores
    válidos — evita que alguien guarde "semestrl" (typo) o "SEMESTRAL"
    (mayúsculas distintas) sin que nadie se dé cuenta. Al heredar de `str`
    además de `Enum`, SQLModel puede guardarlo directo como texto en la
    base, y en Python lo comparás como si fuera un string normal."""

    MENSUAL = "mensual"
    TRIMESTRAL = "trimestral"
    SEMESTRAL = "semestral"
    AL_FINALIZAR = "al_finalizar"


class Banco(str, Enum):
    BBVA = "BBVA"
    SANTANDER = "Santander"
    OTRO = "Otro"


class ObligacionNegociable(SQLModel, table=True):

    # PK: id
    id: Optional[int] = Field(default=None, primary_key=True)

    # Opcional
    ticker: Optional[str] = None
    fecha_inicio: Optional[date] = None

    # Obligatorios
    denominacion: str

    empresa: str

    tasa_nominal_anual: float

    fecha_vencimiento: date

    monto_nominal: float

    # por ahora a mano, después lo automatizo
    precio_compra_mercado_secundario: Optional[float] = None

    frecuencia_pago: FrecuenciaPago = FrecuenciaPago.AL_FINALIZAR

    banco: Banco