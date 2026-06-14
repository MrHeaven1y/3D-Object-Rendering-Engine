from pydantic import BaseModel, Field, conint
from typing import Dict, Any, Optional

StepsType = conint(ge=1, le=10000)
ComplexityType = conint(ge=1, le=10)


class SimulationConfig(BaseModel):
        name: str = Field(..., description="Human-friendly name")
        steps: StepsType = 100
        complexity: ComplexityType = 3
        params: Dict[str, Any] = {}

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
    resutl: Dict[str, Any]