from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import crear_tablas
from app.routers import bonos

app = FastAPI(title="ON Tracker")

# Para evitar error CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(bonos.router)


@app.on_event("startup")
def on_startup():
    # Se ejecuta una sola vez, cuando arranca el servidor: crea las tablas
    # si todavía no existen (no borra nada si ya existían).
    crear_tablas()


@app.get("/health")
def health():
    return {"status": "ok"}