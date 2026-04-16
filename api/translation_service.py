"""
Multilingual Translation Service
Translates between English and 7 Indian regional languages
using the deep-translator library (Google Translate backend).
"""

import traceback

try:
    from deep_translator import GoogleTranslator
    TRANSLATOR_AVAILABLE = True
except ImportError:
    TRANSLATOR_AVAILABLE = False

# Supported language codes and their full names
SUPPORTED_LANGUAGES = {
    "en": {"name": "English", "native": "English", "google_code": "en"},
    "hi": {"name": "Hindi", "native": "हिन्दी", "google_code": "hi"},
    "te": {"name": "Telugu", "native": "తెలుగు", "google_code": "te"},
    "ta": {"name": "Tamil", "native": "தமிழ்", "google_code": "ta"},
    "kn": {"name": "Kannada", "native": "ಕನ್ನಡ", "google_code": "kn"},
    "ml": {"name": "Malayalam", "native": "മലയാളം", "google_code": "ml"},
    "bn": {"name": "Bengali", "native": "বাংলা", "google_code": "bn"},
    "mr": {"name": "Marathi", "native": "मराठी", "google_code": "mr"},
    "gu": {"name": "Gujarati", "native": "ગુજરાતી", "google_code": "gu"},
    "pa": {"name": "Punjabi", "native": "ਪੰਜਾਬੀ", "google_code": "pa"},
}


class TranslationService:
    """Multilingual translation service for Indian languages."""

    def __init__(self):
        self.available = TRANSLATOR_AVAILABLE
        if not self.available:
            print("[WARN] deep-translator not installed. Translation will be unavailable.")
        else:
            print("[OK] Translation service initialized.")

    def translate(self, text: str, source_lang: str = "auto", target_lang: str = "en") -> dict:
        """
        Translate text between supported languages.

        Args:
            text: Text to translate
            source_lang: Source language code (or 'auto' for detection)
            target_lang: Target language code

        Returns:
            Dict with 'translated_text', 'source_lang', 'target_lang', and 'status'.
        """
        if not text or not text.strip():
            return {
                "translated_text": "",
                "source_lang": source_lang,
                "target_lang": target_lang,
                "status": "empty_input",
            }

        # If source and target are the same, return as-is
        if source_lang == target_lang and source_lang != "auto":
            return {
                "translated_text": text,
                "source_lang": source_lang,
                "target_lang": target_lang,
                "status": "same_language",
            }

        if not self.available:
            return {
                "translated_text": text,
                "source_lang": source_lang,
                "target_lang": target_lang,
                "status": "translator_unavailable",
            }

        try:
            src = source_lang if source_lang != "auto" else "auto"
            tgt = self._get_google_code(target_lang)

            translator = GoogleTranslator(source=src, target=tgt)
            translated = translator.translate(text)

            return {
                "translated_text": translated or text,
                "source_lang": source_lang,
                "target_lang": target_lang,
                "status": "success",
            }
        except Exception as e:
            print(f"Translation error: {e}")
            traceback.print_exc()
            return {
                "translated_text": text,
                "source_lang": source_lang,
                "target_lang": target_lang,
                "status": f"error: {str(e)}",
            }

    def translate_to_english(self, text: str, source_lang: str = "auto") -> str:
        """Translate text to English for NLP processing."""
        if source_lang == "en":
            return text
        result = self.translate(text, source_lang=source_lang, target_lang="en")
        return result["translated_text"]

    def translate_from_english(self, text: str, target_lang: str) -> str:
        """Translate English text to target language."""
        if target_lang == "en":
            return text
        result = self.translate(text, source_lang="en", target_lang=target_lang)
        return result["translated_text"]

    def _get_google_code(self, lang_code: str) -> str:
        """Get the Google Translate language code."""
        lang_info = SUPPORTED_LANGUAGES.get(lang_code)
        if lang_info:
            return lang_info["google_code"]
        return lang_code

    def get_supported_languages(self) -> dict:
        """Return dict of supported languages with metadata."""
        return SUPPORTED_LANGUAGES


# Singleton
_translation_service = None


def get_translation_service() -> TranslationService:
    """Get or create the singleton translation service."""
    global _translation_service
    if _translation_service is None:
        _translation_service = TranslationService()
    return _translation_service
