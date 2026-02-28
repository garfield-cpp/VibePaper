from pydantic import BaseModel
from typing import Optional, List

class AIGenerateRequest(BaseModel):
    topic: str
    outline: Optional[str] = None
    length: Optional[int] = 1000
    model: Optional[str] = None
    deep_thinking: Optional[bool] = False

class AIGenerateResponse(BaseModel):
    content: str

class AIConversationRequest(BaseModel):
    message: str
    context: Optional[List[str]] = None
    model: Optional[str] = None
    deep_thinking: Optional[bool] = False

class AIConversationResponse(BaseModel):
    content: str

class AISearchRequest(BaseModel):
    query: str
    model: Optional[str] = None

class AISearchResponse(BaseModel):
    content: str

class AIPaperOutlineRequest(BaseModel):
    content: str
    model: Optional[str] = None

class AIPaperOutlineResponse(BaseModel):
    content: str

class AIGenerateImageRequest(BaseModel):
    prompt: str
    model: Optional[str] = None

class AIGenerateImageResponse(BaseModel):
    content: str
