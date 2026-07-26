from datetime import date, timedelta

import pytest

from app.finance import calcular_tire
from app.models import ObligacionNegociable


def _on_de_prueba(**overrides) -> ObligacionNegociable:
    """Helper para no repetir la creación de una ON de prueba en cada test.
    """
    base = dict(
        ticker="TEST",
        denominacion="ON de prueba",
        empresa="YPF",
        tasa_nominal_anual=7.0,
        monto_nominal=15000.0,
        fecha_vencimiento=date.today() + timedelta(days=365 * 3),
    )
    base.update(overrides)
    return ObligacionNegociable(**base)


def test_regla_de_oro_precio_bajo_par_da_tire_mas_alta():
    on = _on_de_prueba()
    
    tire_par = calcular_tire(on, 100)
    tire_sub_par = calcular_tire(on, 90)
    
    assert(tire_sub_par > tire_par)


def test_regla_de_oro_precio_sobre_par_da_tire_mas_baja():
    on = _on_de_prueba()
    
    tire_par = calcular_tire(on, 100)
    tire_sobre_par = calcular_tire(on, 110)
    
    assert(tire_par > tire_sobre_par)


def test_calcular_tire_con_precio_cero_lanza_error():
    on = _on_de_prueba()
    with pytest.raises(ValueError):
        calcular_tire(on, 0)
    
        
