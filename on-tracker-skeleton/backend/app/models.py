from datetime import date
from typing import Optional
from sqlmodel import Field, SQLModel


class ObligacionNegociable(SQLModel, table=True):
    
    # PK: id
    id: Optional[int] = Field(default=None, primary_key=True)

    # Opcional
    ticker: Optional[str] = None

    # Obligatorios
    denominacion: str
    
    empresa: str

    tasa_nominal_anual: float

    fecha_vencimiento: date

    monto_nominal: float