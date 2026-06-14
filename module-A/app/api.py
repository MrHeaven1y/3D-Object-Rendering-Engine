from fastapi import FastAPI, HTTPException
from .schemas import SimulationConfig, StartResponse, StatusResponse, ResultResponse
from .db import init_db, SessionLocal
from .models import SimulationRun
from .worker import start_simulation, stop_simulation
import datetime

app = FastAPI(title="Module-A Simulation Service")

@app.on_event("startup")
def startup():
    init_db()

@app.post("/simulations", response_model=StartResponse)
def create_simulation(cfg: SimulationConfig):
    session = SessionLocal()
    run = SimulationRun(
        name=cfg.name,
        config=cfg.dict(),
        seed=int(datetime.datetime.utcnow().timestamp())  # default seed
    )
    session.add(run)
    session.commit()
    session.refresh(run)
    start_simulation(run.id, run.config, seed=run.seed)
    session.close()
    return {"run_id": run.id}

@app.get("/simulations/{run_id}", response_model=StatusResponse)
def get_status(run_id: str):
    session = SessionLocal()
    run = session.query(SimulationRun).filter(SimulationRun.id == run_id).first()
    session.close()
    if not run:
        raise HTTPException(status_code=404, detail="Run not found")
    return {
        "run_id": run.id,
        "status": run.status,
        "progress": run.progress,
        "started_at": run.started_at.isoformat() if run.started_at else None,
        "finished_at": run.finished_at.isoformat() if run.finished_at else None,
        "error": run.error
    }

@app.get("/simulations/{run_id}/result", response_model=ResultResponse)
def get_result(run_id: str):
    session = SessionLocal()
    run = session.query(SimulationRun).filter(SimulationRun.id == run_id).first()
    session.close()
    if not run:
        raise HTTPException(status_code=404, detail="Run not found")
    if run.status != "completed":
        raise HTTPException(status_code=409, detail="Result not available yet")
    return {"run_id": run.id, "result": run.result}

@app.post("/simulations/{run_id}/stop")
def stop_run(run_id: str):
    ok = stop_simulation(run_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Run not running or not found")
    return {"stopped": True}
