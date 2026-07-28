import { useEffect, useState } from "react";
import { fetchBonos, reimportarBonos, type Bono } from "../api";
import { analizarON, formatearFechaCorta, formatearUSD } from "../utils/analisis";

function formatearTipoMercado(tipo: string): string {
  if (tipo.toLowerCase() === "primario") return "Primario";
  if (tipo.toLowerCase() === "secundario") return "Secundario";
  return tipo;
}

export function TablaBonos() {
  const [bonos, setBonos] = useState<Bono[]>([]);
  const [error, setError] = useState<string | null>(null);
  const [isImporting, setIsImporting] = useState(false);
  const [expandedId, setExpandedId] = useState<number | null>(null);

  const cargarBonos = () =>
    fetchBonos()
      .then(setBonos)
      .catch(() => {
        setError("No se pudo conectar con el servidor.");
        throw new Error("No se pudo conectar con el servidor.");
      });

  useEffect(() => {
    void cargarBonos();
  }, []);

  const handleReimportar = async () => {
    setIsImporting(true);
    setError(null);

    try {
      await reimportarBonos();
      await cargarBonos();
    } catch {
      setError("No se pudo volver a importar los datos.");
    } finally {
      setIsImporting(false);
    }
  };

  return (
    <div>
      <div className="mb-4 flex justify-end">
        <button
          type="button"
          onClick={handleReimportar}
          disabled={isImporting}
          className="rounded-lg bg-slate-900 px-4 py-2 text-sm font-medium text-white transition hover:bg-slate-700 disabled:cursor-not-allowed disabled:bg-slate-400"
        >
          {isImporting ? "Importando..." : "Reimportar datos"}
        </button>
      </div>

      {error ? <p className="mb-4 text-sm text-red-600">{error}</p> : null}

      <div className="space-y-3">
        {bonos.map((b) => {
          const analisis = analizarON(b);
          const isOpen = expandedId === b.id;
          return (
            <div key={b.id} className="rounded-xl border border-slate-200 bg-white shadow-sm">
              <button
                type="button"
                onClick={() => setExpandedId(isOpen ? null : b.id)}
                className="flex w-full items-center justify-between px-4 py-3 text-left"
              >
                <div>
                  <p className="font-semibold text-slate-900">{b.ticker ?? "—"} · {b.empresa}</p>
                  <p className="text-sm text-slate-500">{b.banco} · {formatearTipoMercado(b.tipo_mercado)}</p>
                </div>
                <div className="text-right text-sm text-slate-500">
                  <p>{formatearFechaCorta(b.fecha_inicio)}</p>
                  <p>Vto. {formatearFechaCorta(b.fecha_vencimiento)}</p>
                </div>
              </button>
              {isOpen && (
                <div className="border-t border-slate-100 px-4 py-4 text-sm text-slate-700">
                  <div className="grid gap-3 md:grid-cols-3">
                    <div className="rounded-lg bg-slate-50 p-3">
                      <p className="text-xs uppercase tracking-wide text-slate-500">Ganancia acumulada</p>
                      <p className="mt-1 text-lg font-semibold text-slate-900">{formatearUSD(analisis.interesesAcumulados)}</p>
                    </div>
                    <div className="rounded-lg bg-slate-50 p-3">
                      <p className="text-xs uppercase tracking-wide text-slate-500">Ganancia esperada al vencimiento</p>
                      <p className="mt-1 text-lg font-semibold text-slate-900">{formatearUSD(analisis.interesesTotales)}</p>
                    </div>
                    <div className="rounded-lg bg-slate-50 p-3">
                      <p className="text-xs uppercase tracking-wide text-slate-500">Valor final estimado</p>
                      <p className="mt-1 text-lg font-semibold text-slate-900">{formatearUSD(analisis.valorFinalEstimado)}</p>
                    </div>
                  </div>
                  <div className="mt-3 flex flex-wrap gap-2 text-xs">
                    <span className="rounded-full bg-teal-100 px-2.5 py-1 font-medium text-teal-700">Rentabilidad: {analisis.rentabilidadTotal.toFixed(2)}%</span>
                    <span className="rounded-full bg-slate-100 px-2.5 py-1 font-medium text-slate-600">Estado: {analisis.estado}</span>
                    <span className="rounded-full bg-slate-100 px-2.5 py-1 font-medium text-slate-600">Progreso: {analisis.porcentajeCompletado.toFixed(0)}%</span>
                    <span className="rounded-full bg-slate-100 px-2.5 py-1 font-medium text-slate-600">Días restantes: {analisis.diasRestantes}</span>
                  </div>
                </div>
              )}
            </div>
          );
        })}
      </div>
    </div>
  );
}
