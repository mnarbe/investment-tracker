from pathlib import Path

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from app.database import get_session
from app.models import ObligacionNegociable
from seed_data import importar as importar_excel

router = APIRouter(prefix="/bonos", tags=["bonos"])


@router.get("", response_model=list)
def listar_bonos(session: Session = Depends(get_session)):
    ons = session.exec(select(ObligacionNegociable)).all()
    return [on.model_dump() for on in ons]


@router.post("/reimportar")
def reimportar_bonos():
    ruta_excel = Path(__file__).resolve().parents[4] / "Libro1.xlsx"
    if not ruta_excel.exists():
        raise HTTPException(status_code=404, detail="No se encontró el archivo Libro1.xlsx")

    importar_excel(str(ruta_excel))
    return {"message": "Datos reimportados correctamente"}