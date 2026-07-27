import sys

import pandas as pd
from sqlmodel import Session

from app.database import crear_tablas, engine
from app.models import ObligacionNegociable


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

            if pd.isna(denominacion) or pd.isna(empresa) or pd.isna(tasa) or pd.isna(vto) or pd.isna(monto):
                print(f"Salteando fila {indice}: falta un dato obligatorio")
                continue
            
            precio = fila["compra MKT SECUNDARIO"]
            on = ObligacionNegociable(
                ticker=fila["ON"] if not pd.isna(fila["ON"]) else None,
                denominacion=denominacion,
                empresa=empresa,
                tasa_nominal_anual=float(tasa),
                fecha_vencimiento=vto.date(),
                monto_nominal=float(monto),
                precio_compra_mercado_secundario=float(precio) if not pd.isna(precio) else None,
            )
            session.add(on)

        session.commit()

    print("Importación terminada")


if __name__ == "__main__":
    ruta = sys.argv[1] if len(sys.argv) > 1 else "..\..\Libro1.xlsx"
    importar(ruta)