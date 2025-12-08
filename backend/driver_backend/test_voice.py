import requests
import base64

# Test voice command
def test_voice_command():
    url = "http://localhost:8000/api/driver/voice/command"
    
    # You'll need to record a .wav file or use an existing one
    with open("test_audio.wav", "rb") as audio_file:
        files = {"audio_file": audio_file}
        params = {"driver_id": "DRV123"}
        
        response = requests.post(url, files=files, params=params)
        print(response.json())

# Test TTS
def test_text_to_speech():
    url = "http://localhost:8000/api/driver/voice/text-to-speech"
    payload = {
        "text": "Shipment SHP123 has been confirmed for pickup",
        "voice": "nova"
    }
    
    response = requests.post(url, json=payload)
    
    with open("response.mp3", "wb") as f:
        f.write(response.content)
    
    print("Audio saved to response.mp3")

if __name__ == "__main__":
    test_text_to_speech()