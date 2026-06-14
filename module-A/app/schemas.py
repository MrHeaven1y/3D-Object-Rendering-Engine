from pydantic import BaseModel, Field 
from typing import Dict, Any, Optional


class SimulationConfig(BaseModel): # startup simulation config class
        name: str = Field(..., description="Human-friendly name") # simulation name
        steps: int = Field(100, ge=1, le=10000) # number steps per unit time, basically how many divison of total fake time 
        complexity: int = Field(3, ge=1, le=10) # resolution control
        params: Dict[str, Any] = {} # addition parameters

class StartResponse(BaseModel):
    run_id: str


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