
from typing import Any
from pydantic import BaseModel


class LoginRequest(BaseModel):
    username: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class ChatRequest(BaseModel):
    message: str


class ChatAction(BaseModel):
    action: str
    action_input: Any = None
    observation: str = ""


class AgentResponse(BaseModel):
    actions: list[ChatAction] = []
    final_answer: str = ""


class ChatResponse(BaseModel):
    response: AgentResponse
