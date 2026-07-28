import type { Bono } from "../api";

export interface AnalisisON {
  interesesAcumulados: number;
  interesesTotales: number;
  valorFinalEstimado: number;
  rentabilidadTotal: number;
  diasTranscurridos: number;
  diasRestantes: number;
  porcentajeCompletado: number;
  estado: "vigente" | "vencida" | "próximamente" | "sin-fecha";
}

function parseIsoDate(iso: string | null): Date | null {
  if (!iso) return null;
  const [year, month, day] = iso.split("-").map(Number);
  return new Date(Date.UTC(year, month - 1, day));
}

function diffDays(start: Date, end: Date): number {
  return Math.round((end.getTime() - start.getTime()) / (1000 * 60 * 60 * 24));
}

export function formatearUSD(monto: number): string {
  return monto.toLocaleString("es-AR", {
    style: "currency",
    currency: "USD",
    maximumFractionDigits: 0,
  });
}

export function formatearFechaCorta(iso: string | null): string {
  if (!iso) return "—";
  return new Date(iso + "T00:00:00").toLocaleDateString("es-AR", {
    day: "2-digit",
    month: "short",
    year: "numeric",
  });
}

export function analizarON(bono: Bono): AnalisisON {
  const today = new Date();
  today.setUTCHours(0, 0, 0, 0);

  const fechaInicio = parseIsoDate(bono.fecha_inicio);
  const fechaVencimiento = parseIsoDate(bono.fecha_vencimiento);

  if (!fechaVencimiento) {
    return {
      interesesAcumulados: 0,
      interesesTotales: 0,
      valorFinalEstimado: bono.monto_nominal,
      rentabilidadTotal: 0,
      diasTranscurridos: 0,
      diasRestantes: 0,
      porcentajeCompletado: 0,
      estado: "sin-fecha",
    };
  }

  const totalDays = fechaInicio ? Math.max(0, diffDays(fechaInicio, fechaVencimiento)) : 0;
  const diasTranscurridos = fechaInicio ? Math.max(0, diffDays(fechaInicio, today)) : 0;
  const diasTranscurridosClamped = totalDays > 0 ? Math.min(diasTranscurridos, totalDays) : 0;
  const diasRestantes = today < fechaVencimiento ? Math.max(0, diffDays(today, fechaVencimiento)) : 0;

  const tasaDecimal = bono.tasa_nominal_anual / 100;
  const interesesAcumulados = fechaInicio ? bono.monto_nominal * tasaDecimal * (diasTranscurridosClamped / 365) : 0;
  const interesesTotales = totalDays > 0 ? bono.monto_nominal * tasaDecimal * (totalDays / 365) : 0;
  const valorFinalEstimado = bono.monto_nominal + interesesTotales;
  const rentabilidadTotal = bono.monto_nominal > 0 ? ((valorFinalEstimado / bono.monto_nominal) - 1) * 100 : 0;
  const porcentajeCompletado = totalDays > 0 ? Math.min(100, (diasTranscurridosClamped / totalDays) * 100) : 0;

  let estado: AnalisisON["estado"] = "vigente";
  if (!fechaInicio) {
    estado = "sin-fecha";
  } else if (today > fechaVencimiento) {
    estado = "vencida";
  } else if (today < fechaInicio) {
    estado = "próximamente";
  }

  return {
    interesesAcumulados,
    interesesTotales,
    valorFinalEstimado,
    rentabilidadTotal,
    diasTranscurridos: diasTranscurridosClamped,
    diasRestantes,
    porcentajeCompletado,
    estado,
  };
}
