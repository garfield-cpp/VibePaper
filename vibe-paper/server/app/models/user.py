from pydantic import BaseModel, Field
from datetime import datetime

class User(BaseModel):
    id: str
    username: str
    email: str
    password_hash: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
