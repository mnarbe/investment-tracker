from fastapi import APIRouter, Depends
from sqlmodel import Session, select

from app.database import get_session
from app.models import ObligacionNegociable

router = APIRouter(prefix="/bonos", tags=["bonos"])


@router.get("", response_model=list)
def listar_bonos(session: Session = Depends(get_session)):
    ons = session.exec(select(ObligacionNegociable)).all()
    return [on.model_dump() for on in ons]