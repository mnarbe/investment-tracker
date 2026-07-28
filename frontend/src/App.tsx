import { useState } from "react";
import { Dashboard } from "./components/Dashboard";
import { TablaBonos } from "./components/TablaBonos";
import { ProximosPagos } from "./components/ProximosPagos";
import { Rendimiento } from "./components/Rendimiento";

type Vista = "dashboard" | "tabla" | "pagos" | "rendimiento";

function App() {
  const [vista, setVista] = useState<Vista>("dashboard");

  return (
    <div className="min-h-screen bg-slate-50">
      <header className="border-b border-slate-200 bg-white">
        <div className="mx-auto flex max-w-6xl items-center justify-between px-6 py-4">
          <div>
            <h1 className="text-lg font-semibold text-slate-900">ON Tracker</h1>
            <p className="text-xs text-slate-400">Seguimiento de Obligaciones Negociables</p>
          </div>
          <nav className="flex flex-wrap gap-1 rounded-lg bg-slate-100 p-1">
            {([["dashboard", "Resumen"], ["tabla", "Mis ONs"], ["pagos", "Próximos pagos"], ["rendimiento", "Rendimiento"]] as [Vista, string][]).map(([key, label]) => (
              <button key={key} onClick={() => setVista(key)}
                className={`rounded-md px-3 py-1.5 text-sm font-medium transition ${vista === key ? "bg-white text-slate-900 shadow-sm" : "text-slate-500 hover:text-slate-700"}`}>
                {label}
              </button>
            ))}
          </nav>
        </div>
      </header>
      <main className="mx-auto max-w-6xl px-6 py-8">
        {vista === "dashboard" && <Dashboard />}
        {vista === "tabla" && <TablaBonos />}
        {vista === "pagos" && <ProximosPagos />}
        {vista === "rendimiento" && <Rendimiento />}
      </main>
    </div>
  );
}

export default App;