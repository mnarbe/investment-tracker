import { useEffect, useState } from "react";
import { fetchBonos, reimportarBonos, type Bono } from "../api";

function formatearFecha(iso: string | null): string {
  if (!iso) return "—";
  return new Date(iso + "T00:00:00").toLocaleDateString("es-AR");
}

function formatearTipoMercado(tipo: string): string {
  if (tipo.toLowerCase() === "primario") return "Primario";
  if (tipo.toLowerCase() === "secundario") return "Secundario";
  return tipo;
}

export function TablaBonos() {
  const [bonos, setBonos] = useState<Bono[]>([]);
  const [error, setError] = useState<string | null>(null);
  const [isImporting, setIsImporting] = useState(false);

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

      <div className="overflow-x-auto rounded-xl border border-slate-200 bg-white shadow-sm">
      <table className="min-w-full divide-y divide-slate-200 text-sm">
        <thead className="bg-slate-50 text-left text-xs font-medium uppercase tracking-wide text-slate-500">
          <tr>
            <th className="px-4 py-3">Ticker</th>
            <th className="px-4 py-3">Emisor</th>
            <th className="px-4 py-3">Banco</th>
            <th className="px-4 py-3">Tipo mercado</th>
            <th className="px-4 py-3">Inicio</th>
            <th className="px-4 py-3">Vencimiento</th>
            <th className="px-4 py-3 text-right">Monto</th>
            <th className="px-4 py-3 text-right">Tasa</th>
          </tr>
        </thead>
        <tbody className="divide-y divide-slate-100">
          {bonos.map((b) => (
            <tr key={b.id} className="hover:bg-slate-50">
              <td className="px-4 py-3 font-medium text-slate-900">{b.ticker ?? "—"}</td>
              <td className="px-4 py-3 text-slate-700">{b.empresa}</td>
              <td className="px-4 py-3 text-slate-700">{b.banco}</td>
              <td className="px-4 py-3 text-slate-700">{formatearTipoMercado(b.tipo_mercado)}</td>
              <td className="px-4 py-3 text-slate-700">{formatearFecha(b.fecha_inicio)}</td>
              <td className="px-4 py-3 text-slate-700">{formatearFecha(b.fecha_vencimiento)}</td>
              <td className="px-4 py-3 text-right text-slate-700">{b.monto_nominal.toLocaleString("es-AR")}</td>
              <td className="px-4 py-3 text-right text-slate-700">{b.tasa_nominal_anual.toFixed(2)}%</td>
            </tr>
          ))}
        </tbody>
      </table>
      </div>
    </div>
  );
}
