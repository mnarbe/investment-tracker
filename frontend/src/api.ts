import axios from "axios";


const api = axios.create({ baseURL: import.meta.env.VITE_API_URL ?? "http://localhost:8000" });

export interface Bono {
  id: number;
  ticker: string | null;
  denominacion: string;
  empresa: string;
  banco: string;
  tasa_nominal_anual: number;
  monto_nominal: number;
  fecha_vencimiento: string;
  precio_compra_mercado_secundario: number | null;
  tire_actual: number | null;
}

export interface ResumenDashboard {
  total_invertido: number;
  intereses_proximos_12_meses: number;
  cantidad_ons: number;
  por_banco: Record<string, number>;
  por_empresa: Record<string, number>;
}

export const fetchBonos = () => api.get<Bono[]>("/bonos").then((r) => r.data);

export const fetchResumen = () =>
  api.get<ResumenDashboard>("/dashboard/resumen").then((r) => r.data);

export const actualizarPrecio = (id: number, precio: number) =>
  api
    .patch<Bono>(`/bonos/${id}/precio`, { precio_compra_mercado_secundario: precio })
    .then((r) => r.data);

export interface EventoPago {
  fecha: string;
  on_id: number;
  ticker: string | null;
  empresa: string;
  cupon: number;
  amortizacion: number;
}

export const fetchCalendario = () =>
  api.get<EventoPago[]>("/dashboard/calendario-pagos").then((r) => r.data);