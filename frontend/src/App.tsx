import { useEffect, useState } from "react";

interface Bono {
  id: number;
  ticker: string | null;
  denominacion: string;
  empresa: string;
  tasa_nominal_anual: number;
  monto_nominal: number;
  fecha_vencimiento: string;
  tire_actual: number | null;
}

function App() {
  const [bonos, setBonos] = useState<Bono[]>([]);

  useEffect(() => {
    fetch("http://localhost:8000/bonos")
    .then((respuesta) => respuesta.json())
    .then((datos) => setBonos(datos))
    .catch((error) => {
      console.error("Error al cargar bonos:", error);
    });
  }, []);

  return (
    <div style={{ padding: 24, fontFamily: "sans-serif" }}>
      <h1>Mis Obligaciones Negociables</h1>
      <table style={{ borderCollapse: "collapse", width: "100%" }}>
        <thead>
          <tr>
            <th style={{ textAlign: "left", borderBottom: "1px solid #ccc" }}>Ticker</th>
            <th style={{ textAlign: "left", borderBottom: "1px solid #ccc" }}>Empresa</th>
            <th style={{ textAlign: "right", borderBottom: "1px solid #ccc" }}>Monto</th>
            <th style={{ textAlign: "right", borderBottom: "1px solid #ccc" }}>Tasa</th>
            <th style={{ textAlign: "right", borderBottom: "1px solid #ccc" }}>TIRE</th>
            <th style={{ textAlign: "left", borderBottom: "1px solid #ccc" }}>Vencimiento</th>
          </tr>
        </thead>
        <tbody>
          {bonos.map((b) => (
            <tr key={b.id}>
              <td>{b.ticker ?? "—"}</td>
              <td>{b.empresa}</td>
              <td style={{ textAlign: "right" }}>{b.monto_nominal}</td>
              <td style={{ textAlign: "right" }}>{b.tasa_nominal_anual}%</td>
              <td style={{ textAlign: "right" }}>
                {b.tire_actual !== null ? `${b.tire_actual}%` : "—"}
              </td>
              <td>{b.fecha_vencimiento}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default App;