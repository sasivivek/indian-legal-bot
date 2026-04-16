"""
Text-to-Speech Service
Generates audio responses in multiple Indian languages using gTTS.
Returns audio as base64-encoded MP3 data.
"""

import io
import base64
import traceback

try:
    from gtts import gTTS
    GTTS_AVAILABLE = True
except ImportError:
    GTTS_AVAILABLE = False

# Language code mapping for gTTS
GTTS_LANGUAGE_MAP = {
    "en": "en",
    "hi": "hi",
    "te": "te",
    "ta": "ta",
    "kn": "kn",
    "ml": "ml",
    "bn": "bn",
    "mr": "mr",
    "gu": "gu",
    "pa": "pa",
}


class TTSService:
    """Text-to-Speech service for Indian languages."""

    def __init__(self):
        self.available = GTTS_AVAILABLE
        if not self.available:
            print("[WARN] gTTS not installed. Text-to-Speech will be unavailable.")
        else:
            print("[OK] TTS service initialized.")

    def generate_audio(self, text: str, language: str = "en") -> dict:
        """
        Generate audio from text in the specified language.

        Args:
            text: Text to convert to speech
            language: Language code for TTS

        Returns:
            Dict with 'audio_base64', 'mime_type', and 'status'.
        """
        if not text or not text.strip():
            return {
                "audio_base64": "",
                "mime_type": "audio/mp3",
                "status": "empty_input",
            }

        if not self.available:
            return {
                "audio_base64": "",
                "mime_type": "audio/mp3",
                "status": "tts_unavailable",
            }

        try:
            # Clean text for speech (remove markdown, excessive whitespace)
            clean_text = self._clean_text_for_speech(text)
            if not clean_text:
                return {
                    "audio_base64": "",
                    "mime_type": "audio/mp3",
                    "status": "empty_after_cleaning",
                }

            # Truncate very long text to avoid excessive processing
            max_chars = 5000
            if len(clean_text) > max_chars:
                clean_text = clean_text[:max_chars] + "... For more details, please refer to the text response."

            # Get gTTS language code
            gtts_lang = GTTS_LANGUAGE_MAP.get(language, "en")

            # Generate audio
            tts = gTTS(text=clean_text, lang=gtts_lang, slow=False)

            # Write to buffer
            audio_buffer = io.BytesIO()
            tts.write_to_fp(audio_buffer)
            audio_buffer.seek(0)

            # Encode as base64
            audio_base64 = base64.b64encode(audio_buffer.read()).decode("utf-8")

            return {
                "audio_base64": audio_base64,
                "mime_type": "audio/mp3",
                "status": "success",
            }

        except Exception as e:
            print(f"TTS error: {e}")
            traceback.print_exc()
            return {
                "audio_base64": "",
                "mime_type": "audio/mp3",
                "status": f"error: {str(e)}",
            }

    def _clean_text_for_speech(self, text: str) -> str:
        """Clean text for natural speech output."""
        import re

        # Remove markdown formatting
        text = re.sub(r"\*\*(.+?)\*\*", r"\1", text)  # Bold
        text = re.sub(r"\*(.+?)\*", r"\1", text)  # Italic
        text = re.sub(r"#{1,6}\s*", "", text)  # Headers
        text = re.sub(r"\[(.+?)\]\(.+?\)", r"\1", text)  # Links
        text = re.sub(r"```[\s\S]*?```", "", text)  # Code blocks
        text = re.sub(r"`(.+?)`", r"\1", text)  # Inline code

        # Remove bullet points and list markers
        text = re.sub(r"^[\s]*[•\-\*]\s*", "", text, flags=re.MULTILINE)
        text = re.sub(r"^[\s]*\d+\.\s*", "", text, flags=re.MULTILINE)

        # Remove emojis/icons
        text = re.sub(r"[📋💡📝📌📚⚠️✅❌🔍]", "", text)

        # Normalize whitespace
        text = re.sub(r"\n+", ". ", text)
        text = re.sub(r"\s+", " ", text)
        text = re.sub(r"\.{2,}", ".", text)

        return text.strip()


# Singleton
_tts_service = None


def get_tts_service() -> TTSService:
    """Get or create the singleton TTS service."""
    global _tts_service
    if _tts_service is None:
        _tts_service = TTSService()
    return _tts_service
