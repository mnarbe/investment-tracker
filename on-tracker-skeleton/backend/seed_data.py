import sys

import pandas as pd
from sqlmodel import Session

from app.database import crear_tablas, engine
from app.models import ObligacionNegociable, Banco, FrecuenciaPago

def _banco_desde_texto(texto) -> Banco | None:
    if not isinstance(texto, str):
        return None
    t = texto.strip().lower()
    if t == "bbva":
        return Banco.BBVA
    if t == "santander":
        return Banco.SANTANDER
    return None
 
def _frecuencia_desde_texto(texto) -> FrecuenciaPago:
    if not isinstance(texto, str):
        return FrecuenciaPago.AL_FINALIZAR  # default si la celda está vacía
    t = texto.lower()
    if "mensual" in t:
        return FrecuenciaPago.MENSUAL
    if "trimestral" in t:
        return FrecuenciaPago.TRIMESTRAL
    if "semestral" in t:
        return FrecuenciaPago.SEMESTRAL
    return FrecuenciaPago.AL_FINALIZAR

def importar(path_excel: str) -> None:
    df = pd.read_excel(path_excel, sheet_name="Inversiones")
    df.columns = [c.strip() for c in df.columns]

    crear_tablas()

    with Session(engine) as session:
        for indice, fila in df.iterrows():
            
            denominacion = fila["denominación"]
            empresa = fila["empresa"]
            tasa = fila["tasa"]
            vto = fila["vto"]
            monto = fila["Monto"]
            banco = _banco_desde_texto(fila["cuenta en"])
            frecuencia = _frecuencia_desde_texto(fila["pago intereses"])

            if pd.isna(denominacion) or pd.isna(empresa) or pd.isna(tasa) or pd.isna(vto) or pd.isna(monto) or pd.isna(banco):
                print(f"Salteando fila {indice}: falta un dato obligatorio")
                continue
            
            
            precio = fila["compra MKT SECUNDARIO"]
            on = ObligacionNegociable(
                ticker=fila["ON"] if not pd.isna(fila["ON"]) else None,
                denominacion=denominacion,
                empresa=empresa.strip(),
                tasa_nominal_anual=float(tasa),
                fecha_vencimiento=vto.date(),
                monto_nominal=float(monto),
                precio_compra_mercado_secundario=float(precio) if not pd.isna(precio) else None,
                banco=banco,
                frecuencia_pago=frecuencia
            )
            session.add(on)

        session.commit()

    print("Importación terminada")


if __name__ == "__main__":
    ruta = sys.argv[1] if len(sys.argv) > 1 else "..\..\Libro1.xlsx"
    importar(ruta)