from datetime import date

from app.models import ObligacionNegociable


def test_guardar_y_leer_on(session):
    # ===ARRANGE===
    
    # YPF - vencimiento largo, cupón medio
    on_ypf = ObligacionNegociable(
        ticker="YMCQD",
        denominacion="ON YPF clase 42",
        empresa="YPF",
        tasa_nominal_anual=7.0,
        fecha_inicio=date(2023, 3, 2),
        fecha_vencimiento=date(2029, 3, 2),
        monto_nominal=15000.0,
    )

    # Pampa Energía - tasa más baja
    on_pampa = ObligacionNegociable(
        ticker="MGC2D",
        denominacion="ON Pampa Energía Clase 9",
        empresa="Pampa Energía",
        tasa_nominal_anual=5.0,
        fecha_inicio=date(2024, 6, 15),
        fecha_vencimiento=date(2027, 6, 15),
        monto_nominal=10000.0,
    )

    # CGC - tasa alta, perfil de mayor riesgo
    on_cgc = ObligacionNegociable(
        ticker="CGCXD",
        denominacion="ON Compañía General de Combustibles",
        empresa="CGC",
        tasa_nominal_anual=12.0,
        fecha_inicio=date(2025, 11, 1),
        fecha_vencimiento=date(2028, 11, 1),
        monto_nominal=8000.0,
    )
    
    # ===ACT (guardar)===
    
    session.add(on_ypf)
    session.add(on_pampa)
    session.add(on_cgc)
    session.commit()
    
    # ===ACT (get)===
    
    ypf_encontrada = session.get(ObligacionNegociable, on_ypf.id)
    pampa_encontrada = session.get(ObligacionNegociable, on_pampa.id)
    cgc_encontrada = session.get(ObligacionNegociable, on_cgc.id)

    # ===ASSERT===
    assert ypf_encontrada is not None
    assert ypf_encontrada.empresa == "YPF"
    assert ypf_encontrada.monto_nominal == 15000
    
    assert pampa_encontrada is not None
    assert pampa_encontrada.empresa == "Pampa Energía"
    assert pampa_encontrada.monto_nominal == 10000
    
    assert cgc_encontrada is not None
    assert cgc_encontrada.empresa == "CGC"
    assert cgc_encontrada.monto_nominal == 8000
