from datetime import date
from enum import Enum
from typing import Optional

from sqlmodel import Field, SQLModel


class FrecuenciaPago(str, Enum):
    """ENUM para evitar typos"""

    MENSUAL = "mensual"
    TRIMESTRAL = "trimestral"
    SEMESTRAL = "semestral"
    AL_FINALIZAR = "al_finalizar"


class Banco(str, Enum):
    BBVA = "BBVA"
    SANTANDER = "Santander"
    OTRO = "Otro"


class TipoMercado(str, Enum):
    PRIMARIO = "primario"
    SECUNDARIO = "secundario"


class ObligacionNegociable(SQLModel, table=True):

    # PK: id
    id: Optional[int] = Field(default=None, primary_key=True)

    ticker: Optional[str] = None
    fecha_inicio: Optional[date] = None

    denominacion: str
    empresa: str
    tasa_nominal_anual: float
    fecha_vencimiento: date
    monto_nominal: float
    frecuencia_pago: FrecuenciaPago = FrecuenciaPago.AL_FINALIZAR
    banco: Banco
    tipo_mercado: TipoMercado = TipoMercado.PRIMARIO