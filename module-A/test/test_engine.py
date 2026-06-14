from app.engine import SimulationEngine
import pytest

def test_engine_progress_and_result():
    cfg = {"steps": 10, "complexity": 2}
    engine = SimulationEngine(cfg, seed=42)
    progress = []
    for update in engine.run():
        progress.append(update["progress"])
    assert progress[-1] == 100
