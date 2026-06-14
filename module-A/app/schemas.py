from pydantic import BaseModel, Field, conint
from typing import Dict, Any, Optional

class SimulationConfig(BaseModel):
    
    name: str = Field(..., description="Human-friendly name")
    steps: conint(ge=1, le=10000) = 100
    complexity: conint(ge=1, le=10) = 3
    params: Dict[str, Any] = {}

class StartResponse(BaseModel):
    run_id: str