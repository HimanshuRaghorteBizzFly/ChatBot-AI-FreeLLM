"""
Speech Studio service.
Provides Text-to-Speech (TTS via gTTS) and Speech-to-Text (STT via Groq Whisper).
"""
import time
from pathlib import Path
from typing import Dict, Any, Optional
from gtts import gTTS
from backend.config import AUDIO_DIR
from backend.providers.registry import registry
from backend.repositories.storage import save_generated_media, log_usage

def generate_text_to_speech(text: str, language: str = "en", accent: str = "com", slow: bool = False) -> Dict[str, Any]:
    """
    Converts text to spoken audio and saves locally for playback.
    """
    if not text.strip():
        return {"path": None, "error": "Please enter text to speak.", "notice": "Please enter text."}

    timestamp = int(time.time() * 1000)
    filename = f"speech_{timestamp}.mp3"
    filepath = AUDIO_DIR / filename

    try:
        tts = gTTS(text=text, lang=language, tld=accent, slow=slow)
        tts.save(str(filepath))

        save_generated_media("audio", text[:100], "SpeechStudio", "Neural-TTS", str(filepath))
        log_usage("SpeechStudio", "Neural-TTS", "audio", cost_estimate=0.0)

        return {
            "path": str(filepath),
            "filename": filename,
            "error": None,
            "notice": "Voice synthesized successfully!"
        }
    except Exception as e:
        return {"path": None, "error": f"TTS Error: {str(e)}", "notice": str(e)}

def text_to_speech(text: str, lang: str = "en", slow: bool = False) -> Dict[str, Any]:
    return generate_text_to_speech(text=text, language=lang, slow=slow)

def transcribe_speech_to_text(audio_bytes: bytes, filename: str = "audio.wav") -> Dict[str, Any]:
    """
    Transcribes audio bytes to text using Groq Whisper Large V3.
    """
    groq = registry.get_provider("Groq")
    if not groq:
        return {"transcript": "", "text": "", "error": "Groq provider not initialized."}

    transcript = groq.transcribe_audio(audio_bytes, filename=filename)
    if "⚠️" in transcript:
        return {"transcript": transcript, "text": transcript, "error": transcript}

    log_usage("Groq", "whisper-large-v3", "speech_to_text", cost_estimate=0.0)
    return {"transcript": transcript, "text": transcript, "error": None}

def transcribe_audio(audio_bytes: bytes, filename: str = "audio.wav") -> Dict[str, Any]:
    return transcribe_speech_to_text(audio_bytes=audio_bytes, filename=filename)
