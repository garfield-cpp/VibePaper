from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class Version(BaseModel):
    id: str
    paper_id: str
    title: str
    content: str
    outline: Optional[str] = None
    created_by: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    version_number: int
