from fastapi.testclient import TestClient

from app.main import app

# FastAPI permite testear las funciones sin launchear el servidor en serio
client = TestClient(app)

def test_health():
    respuesta = client.get("/health")
    
    assert(respuesta.status_code == 200)
    assert(respuesta.json() == {"status":"ok"})
    