from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import crear_tablas
from app.routers import bonos, dashboard

@asynccontextmanager
async def lifespan(app: FastAPI):
    crear_tablas()
    yield

app = FastAPI(title="ON Tracker", lifespan=lifespan)

# Para evitar error CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(bonos.router)
app.include_router(dashboard.router)


@app.get("/health")
def health():
    return {"status": "ok"}