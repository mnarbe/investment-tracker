import { useEffect, useState } from "react";
import { fetchCalendario, type EventoPago } from "../api";

function formatearFecha(iso: string): string {
  return new Date(iso + "T00:00:00").toLocaleDateString("es-AR", {
    day: "2-digit", month: "short", year: "numeric",
  });
}

function formatearUSD(monto: number): string {
  return monto.toLocaleString("es-AR", { style: "currency", currency: "USD", maximumFractionDigits: 2 });
}

export function ProximosPagos() {
  const [eventos, setEventos] = useState<EventoPago[]>([]);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetchCalendario().then(setEventos).catch(() => setError("No se pudo conectar con el servidor."));
  }, []);

  if (error) return <p className="text-sm text-red-600">{error}</p>;
  if (eventos.length === 0) return <p className="text-sm text-slate-400">No hay pagos futuros cargados.</p>;

  return (
    <div className="space-y-3">
      {eventos.map((e, i) => {
        const hayCapital = e.amortizacion > 0;
        return (
          <div
            key={i}
            className={`flex items-center justify-between rounded-xl border p-4 shadow-sm ${
              hayCapital ? "border-teal-200 bg-teal-50" : "border-slate-200 bg-white"
            }`}
          >
            <div className="flex items-center gap-4">
              <div className="w-24 shrink-0 text-sm font-medium text-slate-700">
                {formatearFecha(e.fecha)}
              </div>
              <div>
                <p className="font-medium text-slate-900">
                  {e.ticker ?? e.empresa} <span className="font-normal text-slate-400">· {e.empresa}</span>
                </p>
                <p className="text-xs text-slate-500">
                  Interés: {formatearUSD(e.cupon)}
                  {hayCapital && <span className="ml-2 font-semibold text-teal-700">+ devolución de capital: {formatearUSD(e.amortizacion)}</span>}
                </p>
              </div>
            </div>
            {hayCapital && (
              <span className="rounded-full bg-teal-600 px-3 py-1 text-xs font-semibold text-white">
                Vence esta ON
              </span>
            )}
          </div>
        );
      })}
    </div>
  );
}