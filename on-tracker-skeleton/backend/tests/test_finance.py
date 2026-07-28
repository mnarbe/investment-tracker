from datetime import date

import pytest

from app.finance import generar_flujo_de_fondos
from app.models import FrecuenciaPago, ObligacionNegociable


def _on_de_prueba(**overrides) -> ObligacionNegociable:
    base = dict(
        ticker="TEST",
        denominacion="ON de prueba",
        empresa="YPF",
        tasa_nominal_anual=7.0,
        monto_nominal=15000.0,
        fecha_vencimiento=date(2027, 1, 1),
        frecuencia_pago=FrecuenciaPago.AL_FINALIZAR,
    )
    base.update(overrides)
    return ObligacionNegociable(**base)


def test_generar_flujo_al_finalizar_devuelve_un_pago_en_vencimiento():
    on = _on_de_prueba(
        frecuencia_pago=FrecuenciaPago.AL_FINALIZAR,
        fecha_vencimiento=date(2026, 1, 1),
        tasa_nominal_anual=10.0,
        monto_nominal=10000.0,
    )

    pagos = generar_flujo_de_fondos(on, desde=date(2025, 1, 1))

    assert len(pagos) == 1
    assert pagos[0].fecha == date(2026, 1, 1)
    assert pagos[0].amortizacion == 10000.0
    assert pytest.approx(pagos[0].cupon, rel=1e-6) == 1000.0


def test_generar_flujo_semestral_incluye_todos_los_pagos_esperados():
    on = _on_de_prueba(
        frecuencia_pago=FrecuenciaPago.SEMESTRAL,
        fecha_vencimiento=date(2026, 1, 1),
        tasa_nominal_anual=12.0,
        monto_nominal=12000.0,
    )

    pagos = generar_flujo_de_fondos(on, desde=date(2025, 1, 1))

    assert [p.fecha for p in pagos] == [date(2025, 1, 1), date(2025, 7, 1), date(2026, 1, 1)]
    assert pagos[-1].amortizacion == 12000.0


def test_generar_flujo_respeta_fecha_inicio_si_es_posterior_a_hoy():
    on = _on_de_prueba(
        frecuencia_pago=FrecuenciaPago.SEMESTRAL,
        fecha_inicio=date(2025, 7, 1),
        fecha_vencimiento=date(2026, 1, 1),
        tasa_nominal_anual=12.0,
        monto_nominal=12000.0,
    )

    pagos = generar_flujo_de_fondos(on, desde=date(2025, 1, 1))

    assert len(pagos) == 2
    assert pagos[0].fecha == date(2025, 7, 1)
    assert pagos[1].fecha == date(2026, 1, 1)

