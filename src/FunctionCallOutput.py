from pydantic import BaseModel
from typing import Any, Dict


class FunctionCallOutput(BaseModel):
    prompt: str
    name: str
    parameters: Dict[str, Any]
