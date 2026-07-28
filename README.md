# ON Tracker / ON Tracker

Español
-------

Aplicación full-stack para el seguimiento de un portfolio de Obligaciones Negociables (ONs). El sistema mantiene la información contractual de cada ON (tasa nominal anual, monto nominal, fecha de inicio, fecha de vencimiento, frecuencia de pago y tipo de mercado —primario/secundario—) y genera el calendario de pagos futuros (cupones y amortizaciones). Los datos provienen de una planilla Excel importada al backend.

Funcionalidad principal
- Datos contractuales: `tasa_nominal_anual`, `monto_nominal`, `fecha_inicio`, `fecha_vencimiento`, `frecuencia_pago`, `tipo_mercado`.
- Generación de calendario de pagos futuros (cupones y amortizaciones) desde la información contractual.
- Dashboard con totales por banco y por emisor, y resumen de intereses próximos 12 meses.
- Importador desde Excel que mapea columnas flexibles (ver `on-tracker-skeleton/backend/seed_data.py`).

Desarrollo local

Backend
```bash
cd on-tracker-skeleton/backend
python -m venv .venv
.venv\Scripts\Activate.ps1   # Windows (PowerShell)
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Frontend
```bash
cd frontend
npm install
npm run dev
```

Importar desde Excel
```bash
cd on-tracker-skeleton/backend
python seed_data.py "ruta/a/tu/archivo.xlsx"
```

Tests (backend)
```bash
cd on-tracker-skeleton/backend
pytest -q
```

Notas de diseño
- El backend usa `SQLModel` (Pydantic + SQLAlchemy) y FastAPI.
- El importador intenta manejar columnas con nombres flexibles: `tipo de mercado`, `fecha_inicio`, `tasa`, `monto`, `vencimiento`, etc.
- Se prioriza conservar la tasa nominal provista en la planilla; ya no se depende de un precio de mercado para calcular la TIRE.

English
-------

Full‑stack application to track a portfolio of Argentine corporate bonds (Obligaciones Negociables, ONs). The system stores the contractual data for each bond (annual nominal rate, principal amount, start date, maturity date, payment frequency and market type — primary/secondary —) and generates the schedule of future payments (coupons and principal). Data is imported from an Excel spreadsheet into the backend.

Main features
- Contractual data fields: `tasa_nominal_anual` (annual nominal rate), `monto_nominal` (principal), `fecha_inicio` (start date), `fecha_vencimiento` (maturity), `frecuencia_pago` (payment frequency), `tipo_mercado` (market type).
- Generate payment schedule (coupons + principal) from contractual data.
- Dashboard with totals by bank and issuer, and next-12-month interest projection.
- Excel importer with flexible column matching (see `on-tracker-skeleton/backend/seed_data.py`).

Local development

Backend
```bash
cd on-tracker-skeleton/backend
python -m venv .venv
.venv\Scripts\Activate.ps1   # Windows (PowerShell)
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Frontend
```bash
cd frontend
npm install
npm run dev
```

Import from Excel
```bash
cd on-tracker-skeleton/backend
python seed_data.py "path/to/your/file.xlsx"
```

Tests (backend)
```bash
cd on-tracker-skeleton/backend
pytest -q
```

Design notes
- Backend: FastAPI + SQLModel (Pydantic + SQLAlchemy).
- Importer: tolerant to variations in Excel column names; maps `tipo_mercado` and `fecha_inicio` when present.
- The app uses the nominal rate provided in the spreadsheet; it no longer relies on a market price to compute an internal rate of return (TIRE).

If you want, I can also add a short example Excel template and a developer checklist. Want that? 
