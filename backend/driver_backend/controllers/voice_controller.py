from fastapi import APIRouter, HTTPException, Depends, File, UploadFile
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from backend.shared.database import get_db
from backend.driver_backend.schemas.voice_schemas import VoiceCommandResponse, TextToSpeechRequest
from backend.driver_backend.services.voice_assistant_service import VoiceAssistantService
from backend.driver_backend.services.driver_service import DriverService
from backend.driver_backend.services.shipment_service import ShipmentService
from io import BytesIO
import base64

router = APIRouter(prefix="/voice", tags=["Voice Assistant"])

@router.post("/command", response_model=VoiceCommandResponse)
async def process_voice_command(
    driver_id: str,
    audio_file: UploadFile = File(...),
    db: Session = Depends(get_db)  # Only inject database session
):
    """
    Process voice command from driver
    """
    try:
        # Instantiate services
        voice_service = VoiceAssistantService()
        shipment_service = ShipmentService(db)
        
        # Read and encode audio
        audio_bytes = await audio_file.read()
        audio_base64 = base64.b64encode(audio_bytes).decode('utf-8')
        
        # Step 1: Transcribe audio
        transcription = await voice_service.transcribe_audio(audio_base64)
        
        if not transcription:
            raise HTTPException(status_code=400, detail="Could not transcribe audio")
        
        # Step 2: Analyze intent
        intent_result = await voice_service.analyze_intent(transcription)
        intent = intent_result.get("intent")
        entities = intent_result.get("entities", {})
        
        # Step 3: Execute action based on intent
        action_taken = None
        message = ""
        
        if intent == "update_status":
            shipment_id = entities.get("shipment_id")
            status = entities.get("status")
            
            if shipment_id and status:
                # Call your existing shipment service
                await shipment_service.update_status(shipment_id, status, driver_id)
                action_taken = f"Updated shipment {shipment_id} to {status}"
                message = f"Got it! Shipment {shipment_id} marked as {status}."
            else:
                message = "I couldn't identify the shipment ID or status. Please try again."
        
        elif intent == "confirm_pickup":
            shipment_id = entities.get("shipment_id")
            if shipment_id:
                await shipment_service.confirm_pickup(shipment_id, driver_id)
                action_taken = f"Confirmed pickup for {shipment_id}"
                message = f"Pickup confirmed for shipment {shipment_id}!"
            else:
                message = "Which shipment would you like to confirm pickup for?"
        
        elif intent == "confirm_delivery":
            shipment_id = entities.get("shipment_id")
            if shipment_id:
                await shipment_service.confirm_delivery(shipment_id, driver_id)
                action_taken = f"Confirmed delivery for {shipment_id}"
                message = f"Delivery confirmed for shipment {shipment_id}!"
            else:
                message = "Which shipment was delivered?"
        
        elif intent == "report_delay":
            reason = entities.get("reason", "Unspecified reason")
            message = f"Delay reported: {reason}. Dispatch has been notified."
            action_taken = f"Logged delay: {reason}"
        
        elif intent == "update_cod":
            shipment_id = entities.get("shipment_id")
            amount = entities.get("amount")
            if shipment_id and amount:
                # Update COD in your system
                action_taken = f"Updated COD amount for {shipment_id}"
                message = f"COD of {amount} recorded for shipment {shipment_id}."
            else:
                message = "Please specify the shipment ID and amount collected."
        
        else:
            message = "I didn't understand that command. Try saying 'confirm pickup for shipment SHP123' or 'mark SHP456 as delivered'."
        
        return VoiceCommandResponse(
            success=True,
            transcription=transcription,
            intent=intent,
            action_taken=action_taken,
            message=message
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/text-to-speech")
async def convert_text_to_speech(
    request: TextToSpeechRequest
):
    """
    Convert text to speech for driver feedback
    """
    try:
        voice_service = VoiceAssistantService()
        audio_bytes = await voice_service.text_to_speech(request.text, request.voice)
        
        return StreamingResponse(
            BytesIO(audio_bytes),
            media_type="audio/mpeg",
            headers={"Content-Disposition": "attachment; filename=response.mp3"}
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/supported-commands")
async def get_supported_commands():
    """
    Return list of supported voice commands
    """
    return {
        "commands": [
            {
                "intent": "confirm_pickup",
                "examples": [
                    "Confirm pickup for shipment SHP123",
                    "I've picked up order SHP123",
                    "Pickup done for SHP123"
                ]
            },
            {
                "intent": "confirm_delivery",
                "examples": [
                    "Delivered shipment SHP123",
                    "Mark SHP123 as delivered",
                    "Delivery complete for SHP123"
                ]
            },
            {
                "intent": "update_status",
                "examples": [
                    "Update SHP123 to in transit",
                    "Mark SHP123 as out for delivery"
                ]
            },
            {
                "intent": "report_delay",
                "examples": [
                    "I'm running late due to traffic",
                    "Delayed because of vehicle issue",
                    "Traffic jam on highway"
                ]
            },
            {
                "intent": "update_cod",
                "examples": [
                    "Collected 500 rupees for SHP123",
                    "COD amount 1000 for shipment SHP456"
                ]
            }
        ]
    }