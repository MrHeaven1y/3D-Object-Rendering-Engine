from fastapi.testclient import TestClient
from app.api import app

client = TestClient(app)

def test_create_and_status():
    resp = client.post("/simulations", json={"name":"t1","steps":5,"complexity":1})
    assert resp.status_code == 200
    run_id = resp.json()["run_id"]
    status = client.get(f"/simulations/{run_id}")
    assert status.status_code == 200
    assert "status" in status.json()
