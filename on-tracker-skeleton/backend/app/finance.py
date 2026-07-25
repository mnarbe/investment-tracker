# =============================================================================
# ETAPA 5 — El motor financiero: flujo de fondos y TIRE (caso simple)
# =============================================================================
#
# Repasemos el concepto (está también en tu docx de conceptos):
#
# Cuando comprás una ON en el mercado secundario, pagás un PRECIO hoy y a
# cambio vas a recibir PAGOS FUTUROS (interés + devolución del capital). La
# TIRE es la tasa de interés anual que hace que esos pagos futuros, "traídos
# a valor de hoy", sumen exactamente el precio que pagaste. La fórmula
# general (con muchos pagos) es:
#
#     P = sum_{t=1}^{n} (C_t + A_t) / (1 + r)^t
#
# Por ahora vamos a simplificar al caso de UN SOLO PAGO al vencimiento (t
# años desde hoy), donde la fórmula se reduce a:
#
#     P = (C + A) / (1 + r)^t
#
# Como en este caso solo hay una incógnita (r) y una ecuación, se puede
# DESPEJAR r algebraicamente (no hace falta ningún método numérico todavía
# — eso va a cambiar en la próxima etapa, cuando haya varios pagos).
#
# -----------------------------------------------------------------------
# PARTE 1: generar el pago único
# -----------------------------------------------------------------------
# Necesitamos calcular, para una ObligacionNegociable:
#   - C (cupón/interés): monto_nominal * (tasa_nominal_anual / 100) * años
#     Ojo: tasa_nominal_anual está guardada como "7.0" (para 7%), por eso
#     hay que dividir por 100 antes de usarla en la cuenta.
#     "años" = la cantidad de años entre HOY y fecha_vencimiento.
#   - A (amortización/capital): es simplemente monto_nominal, ya que se
#     devuelve todo junto al final.
#
# ¿Cómo calculo "años entre hoy y una fecha"? Con la librería `datetime`:
#     from datetime import date
#     dias = (fecha_vencimiento - date.today()).days
#     años = dias / 365
#
# TU TAREA — completá la función `calcular_pago_al_vencimiento`:
#   Debe devolver una tupla (cupon, amortizacion, años) — los 3 números que
#   vas a necesitar en la Parte 2 para despejar la TIRE.
#
# -----------------------------------------------------------------------
# PARTE 2: despejar la TIRE
# -----------------------------------------------------------------------
# Partiendo de   P = (C + A) / (1 + r)^t   despejamos r:
#
#     (1 + r)^t = (C + A) / P
#     1 + r     = ((C + A) / P) ^ (1/t)
#     r         = ((C + A) / P) ^ (1/t)  -  1
#
# En Python, "elevar a una potencia" se escribe con `**`, por ejemplo:
#     base ** exponente
#
# El precio de mercado (P) no lo tenemos como "porcentaje de la par" sino
# que hay que convertirlo a un monto en dólares, igual que monto_nominal:
#     precio_en_dolares = monto_nominal * (precio_mercado_pct / 100)
#
# TU TAREA — completá la función `calcular_tire`:
#   1. Llamá a calcular_pago_al_vencimiento(on) para obtener (cupon,
#      amortizacion, años).
#   2. Calculá precio_en_dolares a partir de precio_mercado_pct.
#   3. Aplicá la fórmula despejada de arriba para obtener r.
#   4. Devolvé r como PORCENTAJE (multiplicado por 100), redondeado a 2
#      decimales con round(valor, 2), para que sea comparable con
#      tasa_nominal_anual (que también está en formato "7.0" = 7%).
#
# -----------------------------------------------------------------------
# CÓMO VAS A SABER SI ESTÁ BIEN (antes de escribir tests formales):
# -----------------------------------------------------------------------
# Un chequeo de sentido común que podés hacer a mano en el REPL de Python:
# si precio_mercado_pct = 100 (comprás "a la par"), la TIRE calculada
# debería ser MUY cercana a tasa_nominal_anual (van a diferir apenas, por
# la composición del interés). Si le pasás un precio menor a 100 (bajo la
# par), la TIRE tiene que dar MÁS ALTA que la tasa nominal — es la "regla
# de oro" que ya vimos en tu docx.
# =============================================================================

from datetime import date

from app.models import ObligacionNegociable


def calcular_pago_al_vencimiento(on: ObligacionNegociable) -> tuple[float, float, float]:
    """Devuelve (cupon, amortizacion, años) para un bono que paga todo
    junto al vencimiento."""
    # TODO: calcular los años entre hoy y on.fecha_vencimiento

    # TODO: calcular el cupón (interés) con la fórmula de la Parte 1

    # TODO: devolver (cupon, amortizacion, años)
    pass


def calcular_tire(on: ObligacionNegociable, precio_mercado_pct: float) -> float:
    """Calcula la TIRE (en %) a partir del precio de mercado (% de la par)."""
    # TODO: obtener (cupon, amortizacion, años) llamando a la función de arriba

    # TODO: calcular el precio en dólares a partir de precio_mercado_pct

    # TODO: aplicar la fórmula despejada y devolver r como porcentaje
    pass