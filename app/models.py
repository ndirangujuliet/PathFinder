from pydantic import BaseModel
from typing import Optional, Dict


class USSDRequest(BaseModel):
    sessionId: str
    phoneNumber: str
    networkCode: str
    serviceCode: str
    text: str


class USSDResponse(BaseModel):
    response: str
    action: str = "CON"


class SessionState:
    """In-memory session state management"""
    
    def __init__(self):
        self.sessions: Dict[str, Dict] = {}
    
    def set(self, session_id: str, key: str, value: any) -> None:
        if session_id not in self.sessions:
            self.sessions[session_id] = {}
        self.sessions[session_id][key] = value
    
    def get(self, session_id: str, key: str, default: any = None) -> any:
        if session_id not in self.sessions:
            return default
        return self.sessions[session_id].get(key, default)
    
    def delete(self, session_id: str) -> None:
        if session_id in self.sessions:
            del self.sessions[session_id]


# Global session state instance
session_state = SessionState()
