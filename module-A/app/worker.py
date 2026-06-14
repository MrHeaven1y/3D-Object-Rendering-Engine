import threading
from concurrent.futures import ThreadPoolExecutor
from typing import Callable
from .models import SimulationRun
from .db import SessionLocal
from .engine import SimulationEngine, SimulationError
from sqlalchemy.orm import Session
from sqlalchemy import update
import datetime

_executor = ThreadPoolExecutor(max_workers=4)
_run_locks = {}

def _update_run(session: Session, run_id: str, **kwargs):
    session.query(SimulationRun).filter(SimulationRun.id == run_id).update(kwargs)
    session.commit()

def start_simulation(run_id: str, config: dict, seed: int = None):
    stop_event = threading.Event()
    _run_locks[run_id] = stop_event

    def _task():
        session = SessionLocal()
        try:
            _update_run(session, run_id, status="running", started_at=datetime.datetime.utcnow())
            engine = SimulationEngine(config=config, seed=seed)
            for update in engine.run():
                if stop_event.is_set():
                    _update_run(session, run_id, status="stopped", progress=update["progress"], finished_at=datetime.datetime.utcnow())
                    return
                _update_run(session, run_id, progress=update["progress"])
            # engine.run returns final result via StopIteration.value in generator; handle by running to completion
            # For simplicity, re-run to get final result deterministically (cheap)
            final_engine = SimulationEngine(config=config, seed=seed)
            for _ in final_engine.run():
                pass
            final_result = final_engine.run().__next__() if False else None
        except SimulationError as e:
            _update_run(session, run_id, status="failed", error=str(e), finished_at=datetime.datetime.utcnow())
        except Exception as e:
            _update_run(session, run_id, status="failed", error=str(e), finished_at=datetime.datetime.utcnow())
        else:
            # compute final result deterministically
            final_engine = SimulationEngine(config=config, seed=seed)
            for _ in final_engine.run():
                pass
            # get result by invoking run to completion and catching StopIteration
            try:
                gen = final_engine.run()
                while True:
                    next(gen)
            except StopIteration as si:
                result = si.value if hasattr(si, "value") else {
                    "seed": seed,
                    "note": "result not captured via StopIteration on this Python version"
                }
            _update_run(session, run_id, status="completed", progress=100, result=result, finished_at=datetime.datetime.utcnow())
        finally:
            session.close()
            _run_locks.pop(run_id, None)

    _executor.submit(_task)

def stop_simulation(run_id: str):
    ev = _run_locks.get(run_id)
    if ev:
        ev.set()
        return True
    return False