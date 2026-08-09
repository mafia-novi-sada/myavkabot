import io
from _io import BytesIO

from gtts import gTTS
from gtts.lang import tts_langs


class TextToSpeech:
    _langs: dict[str, str] = tts_langs()

    @classmethod
    def tts_buffer(
        cls, text: str, lang: str = "ru", slow: bool = False
    ) -> io.BytesIO | None:
        if not text or not text.strip():
            print("Text is empty.")
            return None
        if cls.language_supported(lang):
            tts: gTTS = gTTS(text=text, lang=lang, slow=slow)
            mp3_buffer: BytesIO = io.BytesIO()
            tts.write_to_fp(mp3_buffer)
            mp3_buffer.seek(0)
            return mp3_buffer
        print(f'Language "{lang}" is not supported.')
        return None

    @classmethod
    def language_supported(cls, code: str) -> bool:
        return code in cls._langs

    @classmethod
    def resolve_language(cls, code: str) -> str:
        if cls.language_supported(code):
            return cls._langs[code]
        return code

    @classmethod
    def get_language_codes(cls) -> list[str]:
        return list[str](cls._langs.keys())

    @classmethod
    def get_language_names(cls) -> list[str]:
        return list[str](cls._langs.values())

    @classmethod
    def get_languages(cls) -> dict[str, str]:
        return cls._langs.copy()
