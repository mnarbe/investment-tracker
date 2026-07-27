import { useEffect, useState } from "react";
import { PieChart, Pie, Cell, Tooltip, ResponsiveContainer, Legend } from "recharts";
import { fetchResumen, type ResumenDashboard } from "../api";

const COLORES = ["#0f766e", "#0891b2", "#4338ca", "#7c3aed", "#c026d3", "#e11d48", "#ea580c", "#65a30d"];

function formatearUSD(monto: number): string {
  return monto.toLocaleString("es-AR", { style: "currency", currency: "USD", maximumFractionDigits: 0 });
}

function Tarjeta({ titulo, valor, subtitulo }: { titulo: string; valor: string; subtitulo?: string }) {
  return (
    <div className="rounded-xl border border-slate-200 bg-white p-5 shadow-sm">
      <p className="text-sm font-medium text-slate-500">{titulo}</p>
      <p className="mt-1 text-2xl font-semibold text-slate-900">{valor}</p>
      {subtitulo && <p className="mt-1 text-xs text-slate-400">{subtitulo}</p>}
    </div>
  );
}

function GraficoTorta({ titulo, datos }: { titulo: string; datos: Record<string, number> }) {
  const data = Object.entries(datos).map(([name, value]) => ({ name, value })).sort((a, b) => b.value - a.value);
  return (
    <div className="rounded-xl border border-slate-200 bg-white p-5 shadow-sm">
      <p className="mb-3 text-sm font-medium text-slate-500">{titulo}</p>
      <ResponsiveContainer width="100%" height={260}>
        <PieChart>
          <Pie data={data} dataKey="value" nameKey="name" innerRadius={55} outerRadius={90} paddingAngle={2}>
            {data.map((_, i) => <Cell key={i} fill={COLORES[i % COLORES.length]} />)}
          </Pie>
          <Tooltip formatter={(v) => formatearUSD(Number(v))} />
          <Legend layout="vertical" align="right" verticalAlign="middle" wrapperStyle={{ fontSize: 12 }} />
        </PieChart>
      </ResponsiveContainer>
    </div>
  );
}

export function Dashboard() {
  const [resumen, setResumen] = useState<ResumenDashboard | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetchResumen().then(setResumen).catch(() => setError("No se pudo conectar con el servidor."));
  }, []);

  if (error) return <p className="text-sm text-red-600">{error}</p>;
  if (!resumen) return <p className="text-sm text-slate-400">Cargando…</p>;

  return (
    <div className="space-y-6">
      <div className="grid grid-cols-1 gap-4 sm:grid-cols-3">
        <Tarjeta titulo="Total invertido" valor={formatearUSD(resumen.total_invertido)} subtitulo={`${resumen.cantidad_ons} ONs en cartera`} />
        <Tarjeta titulo="Intereses próx. 12 meses" valor={formatearUSD(resumen.intereses_proximos_12_meses)} />
        <Tarjeta titulo="Bancos" valor={String(Object.keys(resumen.por_banco).length)} subtitulo={Object.keys(resumen.por_banco).join(" · ")} />
      </div>
      <div className="grid grid-cols-1 gap-4 lg:grid-cols-2">
        <GraficoTorta titulo="Distribución por banco" datos={resumen.por_banco} />
        <GraficoTorta titulo="Distribución por emisor" datos={resumen.por_empresa} />
      </div>
    </div>
  );
}