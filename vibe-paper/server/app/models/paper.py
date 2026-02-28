from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

class Paper(BaseModel):
    id: str
    title: str
    content: str
    outline: Optional[str] = None
    user_id: str
    collaborators: List[str] = Field(default_factory=list)
    current_editors: List[str] = Field(default_factory=list)
    last_updated_by: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
