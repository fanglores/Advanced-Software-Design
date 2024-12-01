from pydantic import BaseModel
from datetime import datetime


class SessionData(BaseModel):
    username: str
    expires_at: datetime