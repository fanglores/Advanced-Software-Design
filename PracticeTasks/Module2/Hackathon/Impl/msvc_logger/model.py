from pydantic import BaseModel
from typing import Optional

class ILogFile(BaseModel):
    podName: str
    logs: Optional[str] = None
