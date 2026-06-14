from pydantic import BaseModel, Field 
from typing import Dict, Any, Optional


class SimulationConfig(BaseModel):                                  # startup simulation config class
        name: str = Field(..., description="Human-friendly name")   # simulation name
        steps: int = Field(100, ge=1, le=10000)                     # Total number of steps (how many divisions of total fake time)
        complexity: int = Field(3, ge=1, le=10)                     # Level of detail / computational intensity per step
        params: Dict[str, Any] = {}                                 # additional parameters

class StartResponse(BaseModel):
    run_id: str                                                     # Track's simulation id means the unique id for each animation that has played earlier 


class StatusResponse(BaseModel):
    run_id: str                                                     # simulation id
    status: str                                                     # status like queued, running, terminated
    progress: float                                                 # percentage completed the simulation
    started_at: Optional[str]                                       # time sense of starting
    finished_at: Optional[str]                                      # time sense of ending
    error: Optional[str]                                            # error field

# After simulation status = "completed", you request the result.
class ResultResponse(BaseModel):                                    
    run_id: str                                                     # simulation id
    result: Dict[str, Any]                                          # result is a free‑form Dict[str, Any]