import { useEffect, useState } from "react";
import { fetchBonos, type Bono } from "../api";
import { analizarON, formatearUSD } from "../utils/analisis";

export function Rendimiento() {
  const [bonos, setBonos] = useState<Bono[]>([]);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetchBonos().then(setBonos).catch(() => setError("No se pudo conectar con el servidor."));
  }, []);

  if (error) return <p className="text-sm text-red-600">{error}</p>;
  if (bonos.length === 0) return <p className="text-sm text-slate-400">Cargando rendimiento…</p>;

  const totalInvertido = bonos.reduce((acc, bono) => acc + bono.monto_nominal, 0);
  const totalGanado = bonos.reduce((acc, bono) => acc + analizarON(bono).interesesTotales, 0);
  const totalRecuperado = totalInvertido + totalGanado;
  const bonosConAnalisis = bonos
    .map((bono) => ({ bono, analisis: analizarON(bono) }))
    .sort((a, b) => b.analisis.interesesTotales - a.analisis.interesesTotales);
  const maxGanancia = Math.max(...bonosConAnalisis.map(({ analisis }) => analisis.interesesTotales), 1);
  const topBonos = bonosConAnalisis.slice(0, 5);

  return (
    <div className="space-y-6">
      <div className="grid gap-4 md:grid-cols-3">
        <div className="rounded-xl border border-slate-200 bg-white p-5 shadow-sm">
          <p className="text-sm font-medium text-slate-500">Capital invertido</p>
          <p className="mt-2 text-2xl font-semibold text-slate-900">{formatearUSD(totalInvertido)}</p>
        </div>
        <div className="rounded-xl border border-slate-200 bg-white p-5 shadow-sm">
          <p className="text-sm font-medium text-slate-500">Ganancia estimada</p>
          <p className="mt-2 text-2xl font-semibold text-slate-900">{formatearUSD(totalGanado)}</p>
        </div>
        <div className="rounded-xl border border-slate-200 bg-white p-5 shadow-sm">
          <p className="text-sm font-medium text-slate-500">Valor final estimado</p>
          <p className="mt-2 text-2xl font-semibold text-slate-900">{formatearUSD(totalRecuperado)}</p>
        </div>
      </div>

      <div className="grid gap-4 lg:grid-cols-[1.2fr_0.8fr]">
        <div className="rounded-xl border border-slate-200 bg-white p-5 shadow-sm">
          <h2 className="text-lg font-semibold text-slate-900">Ranking de contribución</h2>
          <div className="mt-4 space-y-3">
            {bonosConAnalisis.map(({ bono, analisis }, index) => {
              const participacion = totalGanado > 0 ? (analisis.interesesTotales / totalGanado) * 100 : 0;
              return (
                <div key={bono.id} className="flex flex-col gap-2 rounded-lg border border-slate-100 p-3 md:flex-row md:items-center md:justify-between">
                  <div>
                    <p className="font-medium text-slate-900">#{index + 1} · {bono.ticker ?? "—"} · {bono.empresa}</p>
                    <p className="text-sm text-slate-500">{bono.banco}</p>
                  </div>
                  <div className="flex flex-wrap gap-2 text-sm">
                    <span className="rounded-full bg-slate-100 px-2.5 py-1 text-slate-600">Ganancia: {formatearUSD(analisis.interesesTotales)}</span>
                    <span className="rounded-full bg-teal-100 px-2.5 py-1 text-teal-700">Participación: {participacion.toFixed(1)}%</span>
                  </div>
                </div>
              );
            })}
          </div>
        </div>

        <div className="rounded-xl border border-slate-200 bg-white p-5 shadow-sm">
          <h2 className="text-lg font-semibold text-slate-900">Top 5 aportes esperados</h2>
          <svg viewBox="0 0 320 180" className="mt-4 h-48 w-full">
            {topBonos.map(({ bono, analisis }, index) => {
              const barHeight = Math.max(18, (analisis.interesesTotales / maxGanancia) * 100);
              const x = 30 + index * 58;
              const y = 140 - barHeight;
              return (
                <g key={bono.id}>
                  <rect x={x} y={y} width="36" height={barHeight} rx="6" fill="#0f766e" />
                  <text x={x + 18} y="160" textAnchor="middle" fontSize="10" fill="#64748b">
                    {bono.ticker ?? "ON"}
                  </text>
                </g>
              );
            })}
          </svg>
          <div className="mt-2 space-y-1 text-sm text-slate-600">
            {topBonos.map(({ bono, analisis }) => (
              <div key={bono.id} className="flex items-center justify-between">
                <span>{bono.ticker ?? "ON"}</span>
                <span>{formatearUSD(analisis.interesesTotales)}</span>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}
