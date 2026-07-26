from fastapi import FastAPI

from app.database import crear_tablas
from app.routers import bonos

app = FastAPI(title="ON Tracker")

app.include_router(bonos.router)

@app.on_event("startup")
def on_startup():
    # Se ejecuta una vez solo cuando arranca el servidor
    # si todavía no existen (no borra nada si ya existían)
    crear_tablas()


@app.get("/health")
def health():
    return {"status": "ok"}