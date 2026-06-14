from pydantic import BaseModel, Field
from typing import Dict, Any, Optional


class SimulationConfig(BaseModel):
        name: str = Field(..., description="Human-friendly name")
        steps: int = Field(100, ge=1, le=10000)
        complexity: int = Field(3, ge=1, le=10)
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