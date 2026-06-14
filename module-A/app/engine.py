import random
import time
from typing import Dict, Any, Generator

class SimulationError(Exception):
    pass

def deterministic_rng(seed: int):
    rng = random.Random(seed)
    
    while True:
        yield rng.random()


class SimulationEngine:
    """
    Simple deterministic simulation engine.
    Given a config and seed, yields progress updates and final result.
    """

    def __init__(self, config: Dict[str, Any], seed: int = None):
        
        self.config = config
        self.seed = seed if seed is not None else int(time.time())
        self._rng = deterministic_rng(self.seed)

    def run(self) -> Generator[Dict[str, Any], None, Dict[str, Any]]:
        
        steps = int(self.config.get("steps", 100))
        complexity = int(self.config.get("complexity", 3))
        params = self.config.get("params", {})

        if steps <= 0:
            raise SimulationError("Steps must be > 0")
        
        accumulated = 0.0
        for i in range(1, steps + 1):
            r = next(self._rng)
            delta = (r * complexity) / steps
            accumulated += delta

            yield {
                "progress": int((i / steps) * 100),
                "intermediate": {
                    "step": i,
                    "delta": delta,
                    "accumulated": accumulated
                }
            }

            result = {
                "score": accumulated,
                "params": params,
                "seed": self.seed,
                "summary": f"Completed {steps} steps with complexity {complexity}"
            }

        return result