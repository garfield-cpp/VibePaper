from pydantic import BaseModel, Field
from datetime import datetime

class Operation(BaseModel):
    id: str
    paper_id: str
    user_id: str
    operation_type: str  # insert, delete, update
    position: int
    content: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)
