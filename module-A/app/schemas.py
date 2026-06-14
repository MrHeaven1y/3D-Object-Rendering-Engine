from pydantic import BaseModel, Field 
from typing import Dict, Any, Optional


class SimulationConfig(BaseModel): # startup simulation config class
        name: str = Field(..., description="Human-friendly name") # simulation name
        steps: int = Field(100, ge=1, le=10000)     # Total number of steps (how many divisions of total fake time)
        complexity: int = Field(3, ge=1, le=10)     # Level of detail / computational intensity per step
        params: Dict[str, Any] = {}                 # additional parameters

class StartResponse(BaseModel):
    run_id: str # 


class StatusResponse(BaseModel):
    run_id: str
    status: str
    progress: float
    started_at: Optional[str]
    finished_at: Optional[str]
    error: Optional[str]

class ResultResponse(BaseModel):
    run_id: str
    result: Dict[str, Any]