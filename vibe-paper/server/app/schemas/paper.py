from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class PaperBase(BaseModel):
    title: str
    content: str
    outline: Optional[str] = None

class PaperCreate(PaperBase):
    pass

class PaperUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    outline: Optional[str] = None

class PaperResponse(PaperBase):
    id: str
    user_id: str
    collaborators: list[str]
    current_editors: list[str]
    last_updated_by: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

class VersionBase(BaseModel):
    title: str
    content: str
    outline: Optional[str] = None

class VersionResponse(VersionBase):
    id: str
    paper_id: str
    created_by: str
    created_at: datetime
    version_number: int
    
    class Config:
        from_attributes = True

class CollaboratorRequest(BaseModel):
    collaborator_id: str
