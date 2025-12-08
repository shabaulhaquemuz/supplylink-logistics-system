from pydantic import BaseModel
from typing import Optional, Literal

class VoiceCommandRequest(BaseModel):
    driver_id: str
    audio_data: str  # Base64 encoded audio
    
class VoiceCommandResponse(BaseModel):
    success: bool
    transcription: str
    intent: str
    action_taken: Optional[str] = None
    message: str
    
class TextToSpeechRequest(BaseModel):
    text: str
    voice: Literal["alloy", "echo", "fable", "onyx", "nova", "shimmer"] = "nova"
    
class VoiceIntentResult(BaseModel):
    intent: str  # e.g., "update_status", "report_delay", "get_directions"
    entities: dict  # Extracted information
    confidence: float