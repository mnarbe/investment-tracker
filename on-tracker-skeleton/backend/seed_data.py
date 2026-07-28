# -*- coding: utf-8 -*-
import sys
import os
from datetime import date

import pandas as pd
from sqlmodel import Session, delete

from app.database import crear_tablas, engine
from app.models import Banco, FrecuenciaPago, ObligacionNegociable, TipoMercado


def _banco_desde_texto(texto) -> Banco | None:
    if not isinstance(texto, str):
        return None
    t = texto.strip().lower()
    if t == "bbva":
        return Banco.BBVA
    if t == "santander":
        return Banco.SANTANDER
    return Banco.OTRO
 
def _frecuencia_desde_texto(texto) -> FrecuenciaPago:
    if not isinstance(texto, str):
        return FrecuenciaPago.AL_FINALIZAR
    t = texto.lower()
    if "mensual" in t:
        return FrecuenciaPago.MENSUAL
    if "trimestral" in t:
        return FrecuenciaPago.TRIMESTRAL
    if "semestral" in t:
        return FrecuenciaPago.SEMESTRAL
    return FrecuenciaPago.AL_FINALIZAR


def _parse_numero(valor) -> float | None:
    if pd.isna(valor) or valor is None:
        return None
    if isinstance(valor, (int, float)):
        return float(valor)
    texto = str(valor).strip().replace("$", "").replace("%", "").replace(",", "")
    try:
        return float(texto)
    except ValueError:
        return None


def _parse_fecha(valor) -> date | None:
    if pd.isna(valor) or valor is None:
        return None
    if isinstance(valor, date):
        return valor
    try:
        return pd.to_datetime(valor).date()
    except Exception:
        return None


def _leer_celda(fila, *nombres):
    for nombre in nombres:
        if nombre in fila and not pd.isna(fila[nombre]):
            return fila[nombre]
    return None


def importar(path_excel: str, limpiar_existentes: bool = True) -> None:
    df = pd.read_excel(path_excel, sheet_name="Inversiones")
    df.columns = [c.strip().lower() for c in df.columns]

    crear_tablas()

    with Session(engine) as session:
        if limpiar_existentes:
            session.exec(delete(ObligacionNegociable))
            session.commit()

        for indice, fila in df.iterrows():
            denominacion = _leer_celda(fila, "denominaci�n", "denominacion")
            empresa = _leer_celda(fila, "empresa")
            tasa = _parse_numero(_leer_celda(fila, "tasa", "tasa normal", "tasa mercado primario", "tasa mercado secundario"))
            vto = _parse_fecha(_leer_celda(fila, "vto", "vencimiento", "vencimiento u$", "vencimiento u$s"))
            monto = _parse_numero(_leer_celda(fila, "monto", "monto nominal"))
            inicio = _parse_fecha(_leer_celda(fila, "inicio", "fecha inicio", "fecha_inicio"))
            tipo_mercado_texto = _leer_celda(fila, "tipo de mercado", "tipo mercado", "mercado")
            tipo_mercado = TipoMercado.PRIMARIO
            if isinstance(tipo_mercado_texto, str) and tipo_mercado_texto.strip().lower() == "secundario":
                tipo_mercado = TipoMercado.SECUNDARIO

            banco = _banco_desde_texto(_leer_celda(fila, "cuenta en", "cuenta", "banco"))
            frecuencia = _frecuencia_desde_texto(_leer_celda(fila, "pago intereses"))

            if pd.isna(denominacion) or pd.isna(empresa) or tasa is None or vto is None or monto is None or banco is None:
                print(f"Salteando fila {indice}: falta un dato obligatorio")
                continue

            on = ObligacionNegociable(
                ticker=_leer_celda(fila, "on"),
                denominacion=str(denominacion).strip(),
                empresa=str(empresa).strip(),
                tasa_nominal_anual=tasa,
                fecha_vencimiento=vto,
                monto_nominal=monto,
                banco=banco,
                frecuencia_pago=frecuencia,
                tipo_mercado=tipo_mercado,
                fecha_inicio=inicio,
            )
            session.add(on)

        session.commit()

    print("Importaci�n terminada")


if __name__ == "__main__":
    ruta = sys.argv[1] if len(sys.argv) > 1 else os.path.join("..", "..", "Libro1.xlsx")
    importar(ruta)
