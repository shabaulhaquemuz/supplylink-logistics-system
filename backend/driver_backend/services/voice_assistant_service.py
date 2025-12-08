import base64
import json
import re
import os
from pathlib import Path
from typing import Optional, Tuple
from openai import OpenAI
from io import BytesIO
from dotenv import load_dotenv

# Load .env file explicitly
env_path = Path(__file__).parent.parent.parent / '.env'
load_dotenv(dotenv_path=env_path)

# Get API key
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Initialize OpenAI client
if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY not found in environment variables. Please set it in .env file.")

client = OpenAI(api_key=OPENAI_API_KEY)

class VoiceAssistantService:
    
    @staticmethod
    async def transcribe_audio(audio_base64: str) -> str:
        """
        Convert base64 audio to text using OpenAI Whisper
        """
        try:
            # Decode base64 audio
            audio_bytes = base64.b64decode(audio_base64)
            audio_file = BytesIO(audio_bytes)
            audio_file.name = "audio.wav"  # Whisper needs a filename
            
            # Transcribe using Whisper
            transcription = client.audio.transcriptions.create(
                model="whisper-1",
                file=audio_file,
                language="en"  # Change if needed
            )
            
            return transcription.text
            
        except Exception as e:
            raise Exception(f"Transcription failed: {str(e)}")
    
    @staticmethod
    async def analyze_intent(transcription: str) -> dict:
        """
        Use GPT to understand driver's intent from transcription
        """
        system_prompt = """You are a logistics voice assistant for delivery drivers. 
        Analyze the driver's speech and extract:
        1. Intent (update_status, report_delay, request_help, get_route, report_issue, confirm_pickup, confirm_delivery, update_cod)
        2. Entities (shipment_id, status, reason, amount, etc.)
        
        Respond ONLY in JSON format:
        {
            "intent": "intent_name",
            "entities": {"key": "value"},
            "confidence": 0.95
        }
        """
        
        try:
            response = client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": f"Driver said: {transcription}"}
                ],
                temperature=0.3
            )
            
            result = json.loads(response.choices[0].message.content)
            return result
            
        except Exception as e:
            return {
                "intent": "unknown",
                "entities": {},
                "confidence": 0.0
            }
    
    @staticmethod
    async def text_to_speech(text: str, voice: str = "nova") -> bytes:
        """
        Convert text response to speech
        """
        try:
            response = client.audio.speech.create(
                model="tts-1",
                voice=voice,
                input=text
            )
            
            return response.content
            
        except Exception as e:
            raise Exception(f"TTS failed: {str(e)}")
    
    @staticmethod
    def extract_shipment_id(text: str) -> Optional[str]:
        """
        Extract shipment ID from text using regex
        """
        # Match patterns like: SHP123, SHIP-456, etc.
        patterns = [
            r'SHP[-_]?\d+',
            r'SHIP[-_]?\d+',
            r'shipment\s+(\w+)',
            r'order\s+(\w+)'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return match.group(0) if '-' in pattern or '_' in pattern else match.group(1)
        
        return None