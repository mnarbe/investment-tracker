import { useEffect, useState } from "react";
import { actualizarPrecio, fetchBonos, type Bono } from "../api";

function formatearFecha(iso: string): string {
  return new Date(iso + "T00:00:00").toLocaleDateString("es-AR");
}

function EditorPrecio({ bono, onGuardado }: { bono: Bono; onGuardado: (b: Bono) => void }) {
  const [editando, setEditando] = useState(false);
  const [valor, setValor] = useState(String(bono.precio_compra_mercado_secundario ?? ""));
  const [guardando, setGuardando] = useState(false);

  if (!editando) {
    return (
      <button onClick={() => setEditando(true)} className="text-slate-600 underline decoration-dotted hover:text-slate-900">
        {bono.precio_compra_mercado_secundario ? `${bono.precio_compra_mercado_secundario}%` : "cargar precio"}
      </button>
    );
  }

  return (
    <form
      onSubmit={async (e) => {
        e.preventDefault();
        setGuardando(true);
        try {
          const actualizado = await actualizarPrecio(bono.id, Number(valor));
          onGuardado(actualizado);
          setEditando(false);
        } finally {
          setGuardando(false);
        }
      }}
      className="flex items-center gap-1"
    >
      <input autoFocus type="number" step="0.01" value={valor} onChange={(e) => setValor(e.target.value)}
        className="w-16 rounded border border-slate-300 px-1 py-0.5 text-xs" />
      <button type="submit" disabled={guardando} className="rounded bg-teal-700 px-2 py-0.5 text-xs text-white hover:bg-teal-800">✓</button>
    </form>
  );
}

export function TablaBonos() {
  const [bonos, setBonos] = useState<Bono[]>([]);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetchBonos().then(setBonos).catch(() => setError("No se pudo conectar con el servidor."));
  }, []);

  if (error) return <p className="text-sm text-red-600">{error}</p>;

  return (
    <div className="overflow-x-auto rounded-xl border border-slate-200 bg-white shadow-sm">
      <table className="min-w-full divide-y divide-slate-200 text-sm">
        <thead className="bg-slate-50 text-left text-xs font-medium uppercase tracking-wide text-slate-500">
          <tr>
            <th className="px-4 py-3">Ticker</th>
            <th className="px-4 py-3">Emisor</th>
            <th className="px-4 py-3">Banco</th>
            <th className="px-4 py-3 text-right">Monto</th>
            <th className="px-4 py-3 text-right">Tasa</th>
            <th className="px-4 py-3 text-right">Precio secundario</th>
            <th className="px-4 py-3 text-right">TIRE</th>
            <th className="px-4 py-3">Vencimiento</th>
          </tr>
        </thead>
        <tbody className="divide-y divide-slate-100">
          {bonos.map((b) => (
            <tr key={b.id} className="hover:bg-slate-50">
              <td className="px-4 py-3 font-medium text-slate-900">{b.ticker ?? "—"}</td>
              <td className="px-4 py-3 text-slate-700">{b.empresa}</td>
              <td className="px-4 py-3 text-slate-700">{b.banco}</td>
              <td className="px-4 py-3 text-right text-slate-700">{b.monto_nominal.toLocaleString("es-AR")}</td>
              <td className="px-4 py-3 text-right text-slate-700">{b.tasa_nominal_anual.toFixed(2)}%</td>
              <td className="px-4 py-3 text-right"><EditorPrecio bono={b} onGuardado={(a) => setBonos((prev) => prev.map((p) => p.id === a.id ? a : p))} /></td>
              <td className="px-4 py-3 text-right font-medium text-teal-700">{b.tire_actual !== null ? `${b.tire_actual}%` : "—"}</td>
              <td className="px-4 py-3 text-slate-700">{formatearFecha(b.fecha_vencimiento)}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}